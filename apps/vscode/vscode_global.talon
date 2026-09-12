# ^code {user.vscode_workspace}: user.system_command("/opt/homebrew/bin/code {vscode_workspace}")
# ^code {user.vscode_workspace}: user.system_command("/usr/local/bin/cursor {vscode_workspace}")

^code {user.vscode_workspace}: user.switch_to_workspace_by_title_text(vscode_workspace)
^code <user.text>: user.switch_to_workspace_by_title_text(text)
^code open <user.text>:
  user.switcher_focus("Cursor")
  app.window_open()
  sleep(1500ms)
  user.vscode("workbench.action.openRecent")
  sleep(300ms)
  insert(text)
  sleep(100ms)
  key("enter")
