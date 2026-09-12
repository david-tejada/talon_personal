from talon import Module

mod = Module()

mod.list("npm_command", desc="List of npm commands")


# @mod.capture(rule="{user.npm_command}")
# def npm_command(m) -> str:
#     return f"{m.npm_command}"
