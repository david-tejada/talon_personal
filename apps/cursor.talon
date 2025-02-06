app: cursor
-

# Enable/disable AI completion
complete on: user.vscode("editor.action.enableCppGlobally")
complete off: user.vscode("editor.cpp.disableenabled")

# Create new composer/chat
composer new: user.vscode("composer.createNew")
chat new: user.vscode("composer.createNewChat")

# Focus composer/chat
focus composer: user.vscode("workbench.panel.composerViewPane2")
focus chat: user.vscode("workbench.panel.aichat")

# Close composer/chat
[chat | composer] close: user.vscode("aichat.close-sidebar")
