# A voice command for opening the links Claude writes in the Claude desktop
# app (Code tab), by a number shown on each link and file card. A file opens
# in VS Code and a web page opens in the default browser.
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
# Without that rule, links and cards have no numbers and the command finds
# nothing.

import json
import os
import re
import shutil
import subprocess
from pathlib import Path
from urllib.parse import unquote

from talon import Module, app

from .claude_sessions import read_sessions

mod = Module()

# Claude Code keeps each session's transcript here, in a folder named after
# the session's working directory.
TRANSCRIPTS_DIR = Path.home() / ".claude/projects"

# A numbered markdown link, "[[3] name](path)", "[[3] name](path:12)" or
# "[[3] name](https://...)"
NUMBERED_LINK = re.compile(r"\[\[(\d+)\] [^\]]*\]\(([^)\s]+)\)")

# A link target that is a web page rather than a file
WEB_URL = re.compile(r"https?://")


def link_number(title: str) -> int | None:
    """Return n for a link titled "[n] name", or a card titled "TYPE [n] name size" """
    match = re.match(r"(?:\w+ )?\[(\d+)\] ", title)
    return int(match.group(1)) if match else None


def current_session() -> dict | None:
    sessions = read_sessions()
    return max(sessions, key=lambda s: s.get("lastFocusedAt", 0), default=None)


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


@mod.action_class
class Actions:
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
