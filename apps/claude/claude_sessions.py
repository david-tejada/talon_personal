import json
import re
import subprocess
from pathlib import Path

from talon import Context, Module, actions, app, cron

# The Claude desktop app keeps one JSON file per Code session here.
SESSIONS_DIR = (
    Path.home() / "Library/Application Support/Claude/claude-code-sessions"
)

# A session's hint is the "[A] " prefix on its title. Claude adds it in its
# first reply, by a rule in ~/.claude/CLAUDE.md that runs
# ~/.claude/scripts/session_hint.py to pick the first free hint.
HINT = re.compile(r"\[([A-Z]{1,2})\] ")

mod = Module()
mod.list("claude_session", "Titles of Claude Code sessions in the desktop app")

ctx = Context()

last_titles: dict[str, str] = {}


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


def on_ready():
    update_list()
    cron.interval("10s", update_list)


app.register("ready", on_ready)
