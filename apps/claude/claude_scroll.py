# Voice commands for scrolling the chat and the file pane in the Claude
# desktop app (Code tab) without having to put the mouse over them first.
#
# The scroll containers don't expose their scroll position through
# accessibility, so we can't set it directly. Instead we move the pointer over
# the container, send a scroll wheel event there, and move the pointer back.

import math

from talon import Module, actions, app, ctrl, ui

mod = Module()

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
    def claude_scroll(target: str, direction: str, screens: float = 0.66):
        """Scroll the "chat" or the "file" pane up or down by a number of
        screen heights"""
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
