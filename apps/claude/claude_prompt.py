# Voice command for putting the cursor back in the prompt box of the Claude
# desktop app (Code tab), for when focus gets lost, for example after
# cancelling dictation.

from talon import Module, app, ui

mod = Module()


def find_prompt():
    """Return the prompt box in the active window"""

    def walk(el):
        try:
            if el.get("AXRole") == "AXTextArea" and el.get("AXDescription") == "Prompt":
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
    def claude_focus_prompt():
        """Put the cursor in the prompt box"""
        prompt = find_prompt()
        if prompt is None:
            app.notify("No prompt box found")
            return
        prompt.AXFocused = True
