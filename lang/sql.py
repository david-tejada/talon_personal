from talon import Context, Module, actions

mod = Module()

mod.list("sql_keyword", desc="Common SQL keywords")


@mod.capture(rule="<user.text> (and <user.text>)*")
def snake_comma_separated(m) -> str:
    """A non-empty sequence of columns, separated by commas."""
    return ", ".join(
        actions.user.formatted_text(text, "SNAKE_CASE") for text in m.text_list
    )


@mod.capture(rule="{user.sql_keyword}")
def sql_keyword(m) -> str:
    return m.sql_keyword.upper()
