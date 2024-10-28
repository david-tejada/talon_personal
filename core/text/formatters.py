from talon import Module, actions

mod = Module()


@mod.action_class
class Actions:
    def camel(text: str) -> str:
        """Formats text as camelCase"""
        return actions.user.formatted_text(text, "PRIVATE_CAMEL_CASE")

    def pascal(text: str) -> str:
        """Formats text as PascalCase"""
        return actions.user.formatted_text(text, "PRIVATE_CAMEL_CASE")
