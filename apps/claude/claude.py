# Voice commands for the Claude desktop app (Code tab): switching sessions,
# opening numbered links, scrolling, focusing the prompt box and dictating
# with the app's own mic.

import json
import math
import os
import re
import shutil
import subprocess
import time
from pathlib import Path
from urllib.parse import unquote

from talon import Context, Module, actions, app, cron, ctrl, settings, ui

# The Claude desktop app keeps one JSON file per Code session here.
SESSIONS_DIR = (
    Path.home() / "Library/Application Support/Claude/claude-code-sessions"
)

# Claude Code keeps each session's transcript here, in a folder named after
# the session's working directory.
TRANSCRIPTS_DIR = Path.home() / ".claude/projects"

# A session's hint is the "[A] " prefix on its title. Claude adds it in its
# first reply, by a rule in ~/.claude/CLAUDE.md that runs
# ~/.claude/scripts/session_hint.py to pick the first free hint.
HINT = re.compile(r"\[([A-Z]{1,2})\] ")

# A numbered markdown link, "[[3] name](path)", "[[3] name](path:12)" or
# "[[3] name](https://...)"
NUMBERED_LINK = re.compile(r"\[\[(\d+)\] [^\]]*\]\(([^)\s]+)\)")

# A link target that is a web page rather than a file
WEB_URL = re.compile(r"https?://")

# Class names the app gives each scroll container. The file pane shows files
# with CodeMirror, a code editor that runs in the page.
SCROLLER_CLASSES = {
    "chat": {"overflow-y-auto", "[contain:strict]"},
    "file": {"cm-scroller"},
}

# How far the chat moves, in points, for each unit passed to mouse_scroll.
# Measured: 300 units moved it 240 points.
POINTS_PER_SCROLL_UNIT = 0.8

# The largest amount sent in one scroll event, and the most events one
# command sends. "upper all" sends the most.
MAX_SCROLL_UNITS = 30000
MAX_EVENTS = 100

mod = Module()
mod.list("claude_session", "Titles of Claude Code sessions in the desktop app")
mod.tag("claude_dictating", desc="Active while the Claude app's own mic is recording")
mod.setting(
    "claude_dictate_start_grace_ms",
    type=int,
    default=2500,
    desc="Ignore a pop this soon after starting, since the record button's "
    "own start sound can be picked up as one",
)

ctx = Context()

# Only active during a Claude app recording, so the pop override cannot
# affect pops used anywhere else.
ctx_dictating = Context()
ctx_dictating.matches = r"""
tag: user.claude_dictating
"""

last_titles: dict[str, str] = {}
_started_monotonic = 0.0


# Sessions


def read_sessions() -> list[dict]:
    """Return the data of every non-archived session that has a title"""
    sessions = []
    for path in SESSIONS_DIR.glob("*/*/local_*.json"):
        try:
            data = json.loads(path.read_text())
        except (OSError, ValueError):
            continue
        if data.get("title") and not data.get("isArchived"):
            sessions.append(data)
    return sessions


def update_list():
    global last_titles
    # Leave the hint out of the spoken form, so "poppy" takes the title alone.
    titles = {
        HINT.sub("", s["title"], count=1): s["sessionId"] for s in read_sessions()
    }
    if titles == last_titles:
        return
    last_titles = titles
    ctx.lists["user.claude_session"] = actions.user.create_spoken_forms_from_map(
        titles
    )


def find_session_by_hint(hint: str) -> dict | None:
    """Return the data of the session whose title starts with "[hint] " """
    for session in read_sessions():
        match = HINT.match(session["title"])
        if match and match.group(1) == hint.upper():
            return session
    app.notify(f"No session with hint {hint.upper()}")
    return None


def current_session() -> dict | None:
    sessions = read_sessions()
    return max(sessions, key=lambda s: s.get("lastFocusedAt", 0), default=None)


# Numbered links
#
# The app doesn't number anything. The numbers only exist because
# ~/.claude/CLAUDE.md tells Claude to write them, with a rule like this:
#
#   Number every markdown link in your replies, to a file or a web page. Put
#   the number in brackets at the start of the link text:
#   `[[1] vowen.py](plugin/vowen/vowen.py)`. Keep one running count for the
#   whole session, give a link you already numbered the same number every
#   time, and go back to 1 after 99. Before you send a file with
#   SendUserFile, make a symlink to it in your scratchpad named
#   `[n] <file name>`, and send the symlink.
#
# Without that rule, links and cards have no numbers and "follow" finds
# nothing.


def link_number(title: str) -> int | None:
    """Return n for a link titled "[n] name", or a card titled "TYPE [n] name size" """
    match = re.match(r"(?:\w+ )?\[(\d+)\] ", title)
    return int(match.group(1)) if match else None


def transcript_messages(session: dict) -> list[dict]:
    """Return the assistant messages of a session's transcript, oldest first"""
    folder = re.sub(r"[^A-Za-z0-9-]", "-", session["cwd"])
    path = TRANSCRIPTS_DIR / folder / f"{session['cliSessionId']}.jsonl"
    messages = []
    try:
        lines = path.read_text().splitlines()
    except OSError:
        return messages
    for line in lines:
        try:
            entry = json.loads(line)
        except ValueError:
            continue
        if entry.get("type") == "assistant":
            messages.append(entry["message"])
    return messages


def numbered_target(number: int) -> str | tuple[str, int | None] | None:
    """Return the newest link numbered "[number]" in the current session: a
    URL, or the path and optional line of a file from a link or a file card"""
    session = current_session()
    if session is None:
        return None
    for message in reversed(transcript_messages(session)):
        for block in reversed(message.get("content", [])):
            if block.get("type") == "text":
                for n, target in reversed(NUMBERED_LINK.findall(block["text"])):
                    if int(n) != number:
                        continue
                    if WEB_URL.match(target):
                        return target
                    return split_line(target, session["cwd"])
            elif block.get("type") == "tool_use" and block["name"] == "SendUserFile":
                for file in reversed(block["input"].get("files", [])):
                    if link_number(Path(file).name) == number:
                        # Cards are sent as numbered symlinks, so follow them.
                        return os.path.realpath(file), None
    return None


def split_line(target: str, cwd: str) -> tuple[str, int | None]:
    """Split "path:12" into the absolute path and the line"""
    match = re.fullmatch(r"(.+?)(?::(\d+))?", unquote(target))
    path = os.path.join(cwd, os.path.expanduser(match.group(1)))
    line = int(match.group(2)) if match.group(2) else None
    return os.path.normpath(path), line


def git_root(path: str) -> str | None:
    result = subprocess.run(
        ["git", "-C", os.path.dirname(path), "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def open_in_vscode(path: str, line: int | None):
    """Open the file in the VS Code window that has its repository, opening
    the repository in a new window if no window has it"""
    code = shutil.which("code") or "/opt/homebrew/bin/code"
    target = f"{path}:{line}" if line else path
    root = git_root(path)
    args = [code, root, "-g", target] if root else [code, "-g", target]
    subprocess.run(args)


# Window elements


def find_element(role: str, description: str):
    """Return the first element in the active window with this accessibility
    role and description"""

    def walk(el):
        try:
            if el.get("AXRole") == role and el.get("AXDescription") == description:
                return el
            for child in el.children:
                found = walk(child)
                if found is not None:
                    return found
        except Exception:
            return None
        return None

    return walk(ui.active_window().element)


def find_record_button():
    return find_element("AXCheckBox", "Press and hold to record")


def find_scroller(target: str):
    """Return the largest "chat" or "file" scroll container in the active window"""
    scrollers = []

    def walk(el):
        try:
            classes = set(el.get("AXDOMClassList") or [])
            if el.get("AXRole") == "AXGroup" and SCROLLER_CLASSES[target] <= classes:
                scrollers.append(el)
                return
            for child in el.children:
                walk(child)
        except Exception:
            return

    walk(ui.active_window().element)
    return max(
        scrollers,
        key=lambda el: el.get("AXSize").width * el.get("AXSize").height,
        default=None,
    )


@mod.action_class
class Actions:
    def claude_open_session(session_id: str):
        """Open a Claude Code session in the desktop app by its id"""
        subprocess.run(["open", f"claude://code/continue?session={session_id}"])

    def claude_open_session_by_hint(hint: str):
        """Open the session whose title starts with "[hint] " """
        session = find_session_by_hint(hint)
        if session:
            actions.user.claude_open_session(session["sessionId"])

    def claude_archive_session_by_hint(hint: str):
        """Open the session whose title starts with "[hint] " and archive it"""
        session = find_session_by_hint(hint)
        if not session:
            return
        actions.user.claude_open_session(session["sessionId"])
        # Give the app time to switch to the session before archiving it.
        actions.sleep("500ms")
        # The app's own "Archive session" shortcut, which archives the open session.
        actions.key("cmd-alt-a")

    def claude_new_session_by_hint(hint: str):
        """Start a new session in the folder of the session whose title starts
        with "[hint] " """
        session = find_session_by_hint(hint)
        if not session:
            return
        # Opening claude://code/new?folder=... would be simpler, but the app
        # asks to trust the folder every time a link starts a session.
        actions.user.claude_open_session(session["sessionId"])
        actions.sleep("500ms")
        # The app's "New session with current settings" shortcut
        actions.key("cmd-shift-n")

    def claude_open_previous_session():
        """Open the session that was focused before the current one"""
        sessions = sorted(
            read_sessions(), key=lambda s: s.get("lastFocusedAt", 0), reverse=True
        )
        if len(sessions) > 1:
            actions.user.claude_open_session(sessions[1]["sessionId"])

    def claude_follow_numbered_link(number: int):
        """Open the link numbered "[number]" in the Claude chat: a file in VS
        Code, a web page in the default browser"""
        found = numbered_target(number)
        if found is None:
            app.notify(f"No link numbered {number} in this session")
            return
        if isinstance(found, str):
            subprocess.run(["open", found])
            return
        # VS Code opens a missing path as a new empty file, so check first.
        if not os.path.exists(found[0]):
            app.notify(f"File {number} doesn't exist: {found[0]}")
            return
        open_in_vscode(*found)

    def claude_scroll(target: str, direction: str, screens: float = 0.66):
        """Scroll the "chat" or the "file" pane up or down by a number of
        screen heights"""
        # The scroll containers don't expose their scroll position through
        # accessibility, so we can't set it directly. Instead we move the
        # pointer over the container, send a scroll wheel event there, and
        # move the pointer back.
        scroller = find_scroller(target)
        if scroller is None:
            app.notify(f"No {target} to scroll")
            return
        position = scroller.get("AXPosition")
        size = scroller.get("AXSize")
        amount = size.height * screens / POINTS_PER_SCROLL_UNIT
        original = ctrl.mouse_pos()
        ctrl.mouse_move(position.x + size.width / 2, position.y + size.height / 2)
        actions.sleep("20ms")
        # In this app a positive amount scrolls up, the opposite of community's
        # mouse_scroll_down.
        sign = 1 if direction == "up" else -1
        # One huge scroll event overflows and goes the wrong way, so send
        # big scrolls in chunks.
        for _ in range(min(math.ceil(amount / MAX_SCROLL_UNITS), MAX_EVENTS)):
            step = min(amount, MAX_SCROLL_UNITS)
            actions.mouse_scroll(y=sign * step)
            amount -= step
        actions.sleep("20ms")
        ctrl.mouse_move(*original)

    def claude_focus_prompt():
        """Put the cursor in the prompt box"""
        prompt = find_element("AXTextArea", "Prompt")
        if prompt is None:
            app.notify("No prompt box found")
            return
        prompt.AXFocused = True

    def claude_dictate_start():
        """Start recording with the Claude app's own mic instead of Talon"""
        global _started_monotonic
        button = find_record_button()
        if button is None:
            app.notify("No record button found")
            return
        button.perform("AXPress")
        actions.speech.disable()
        _started_monotonic = time.monotonic()
        print(f"[claude_dictate] started at {_started_monotonic}")
        ctx.tags = ["user.claude_dictating"]

    def claude_dictate_submit():
        """Stop the Claude app's recording and send the message"""
        button = find_record_button()
        if button is not None:
            button.perform("AXPress")
        actions.key("enter")
        actions.speech.enable()
        ctx.tags = []


@ctx_dictating.action_class("user")
class DictatingActions:
    def noise_trigger_pop():
        grace = settings.get("user.claude_dictate_start_grace_ms") / 1000.0
        elapsed = time.monotonic() - _started_monotonic
        if elapsed < grace:
            print(f"[claude_dictate] pop ignored at {elapsed:.3f}s (grace {grace}s)")
            return
        print(f"[claude_dictate] pop accepted at {elapsed:.3f}s, submitting")
        actions.user.claude_dictate_submit()


def on_ready():
    update_list()
    cron.interval("10s", update_list)


app.register("ready", on_ready)
