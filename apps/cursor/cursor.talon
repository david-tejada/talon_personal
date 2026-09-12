app: cursor
-

# Enable/disable AI completion
complete on: user.vscode("editor.action.enableCppGlobally")
complete off: user.vscode("editor.cpp.disableenabled")

# Create new chat
chat new: user.vscode("composer.createNew")

# Focus chat
focus chat: user.vscode("workbench.panel.aichat")

# Close chat
close chat: user.vscode("aichat.close-sidebar")
