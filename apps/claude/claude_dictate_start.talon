app.bundle: com.anthropic.claudefordesktop
mode: command
-
# Records with the Claude app's own mic. Bare `dictate` still starts Vowen
# here (plugin/vowen/vowen.talon), so either one is available.
^claude dictate$: user.claude_dictate_start()
