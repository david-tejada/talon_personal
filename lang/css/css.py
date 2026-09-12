from typing import Any, List

from talon import Context, Module, actions

mod = Module()
ctx = Context()

ctx.matches = r"""
code.language: css
code.language: scss
"""


@mod.action_class
class Actions:
    def insert_many_sep(strings: List[str]) -> None:
        """Insert a list of strings separated by a space."""
        for string in strings:
            actions.insert(string)
            actions.insert(" ")
        actions.key("backspace")


@mod.capture(rule="[minus] <number> [point <number>] [{user.css_units}]")
def css_number_unit(m) -> str:
    if "minus" in m:
        result = "-"
    else:
        result = ""
    result = result + ".".join(str(x) for x in m.number_list)
    try:
        result = result + m.css_units
    except AttributeError:
        pass

    return result


@mod.capture(
    rule="<user.number_string> | <self.css_number_unit> | {user.css_values} | {user.css_color_keywords}"
)
def css_value(m) -> str:
    try:
        return m.number_string
    except AttributeError:
        try:
            return m.css_number_unit
        except AttributeError:
            try:
                return m.css_values
            except AttributeError:
                return m.css_color_keywords


@ctx.action_class("user")
class UserActions:
    def code_block():
        actions.insert("{}")
        actions.key("left enter")
