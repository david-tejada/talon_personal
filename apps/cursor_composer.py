from talon import Context, actions

ctx = Context()

ctx.matches = r"""
app: cursor
win.title: /\[(Composer|Chat)\]$/
"""


@ctx.action_class("user")
class UserActions:
    def trigger_command_server_command_execution():
        actions.key("escape")
        actions.next()
