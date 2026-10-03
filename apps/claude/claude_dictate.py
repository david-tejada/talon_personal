import time

from talon import Context, Module, actions, app, settings, ui

mod = Module()
mod.tag("claude_dictating", desc="Active while the Claude app's own mic is recording")
mod.setting(
    "claude_dictate_start_grace_ms",
    type=int,
    default=2500,
    desc="Ignore a pop this soon after starting, since the record button's "
    "own start sound can be picked up as one",
)

ctx = Context()

_started_monotonic = 0.0

# Only active during a Claude app recording, so the pop override cannot
# affect pops used anywhere else.
ctx_dictating = Context()
ctx_dictating.matches = r"""
tag: user.claude_dictating
"""


def find_record_button():
    """Return the Claude app's dictation record button in the active window"""

    def walk(el):
        try:
            if (
                el.get("AXRole") == "AXCheckBox"
                and el.get("AXDescription") == "Press and hold to record"
            ):
                return el
            for child in el.children:
                found = walk(child)
                if found is not None:
                    return found
        except Exception:
            return None
        return None

    return walk(ui.active_window().element)


@mod.action_class
class Actions:
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
