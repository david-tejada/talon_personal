from talon import Module, actions, app, ui

mod = Module()


@mod.action_class
class Actions:
    def switcher_focus_window_by_app_and_title(app_name: str, window_title: str):
        """Focus a window by app name and window title"""
        apps = ui.apps()
        for app in apps:
            if app.name == app_name:
                for window in app.windows():
                    if window_title in window.title:
                        actions.user.switcher_focus_window(window)
                        return
        actions.app.notify(f"No window found for {app_name} with title {window_title}")
