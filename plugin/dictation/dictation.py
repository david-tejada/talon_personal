from talon import Module, actions

mod = Module()


@mod.action_class
class Actions:
    def dictation_start():
        """Start a dictation. Starts Vowen unless the focused app overrides
        this with its own dictation."""
        actions.user.vowen_dictation_start()
