import json
import subprocess
from pathlib import Path

from talon import Context, Module, actions, app, cron

# The Claude desktop app keeps one JSON file per Code session here.
SESSIONS_DIR = (
    Path.home() / "Library/Application Support/Claude/claude-code-sessions"
)

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
    titles = {s["title"]: s["sessionId"] for s in read_sessions()}
    if titles == last_titles:
        return
    last_titles = titles
    ctx.lists["user.claude_session"] = actions.user.create_spoken_forms_from_map(
        titles
    )


@mod.action_class
class Actions:
    def claude_open_session(session_id: str):
        """Open a Claude Code session in the desktop app by its id"""
        subprocess.run(["open", f"claude://code/continue?session={session_id}"])

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
