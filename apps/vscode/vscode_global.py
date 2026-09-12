from talon import Module, actions

mod = Module()
mod.list(
    "vscode_workspace",
    "Vscode workspaces for switching to them quickly",
)


@mod.action_class
class Actions:
    def switch_to_workspace_by_title_text(title_text: str):
        """Focus a window by app name and window title"""
        try:
            actions.user.switcher_focus_window_by_app_and_title(
                "Code", f"{title_text} —"
            )
        except Exception:
            pass
