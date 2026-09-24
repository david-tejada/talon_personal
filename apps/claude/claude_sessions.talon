app.bundle: com.anthropic.claudefordesktop
-
# Search sessions
lisa [<user.text>]:
  key(cmd-shift-k)
  sleep(100ms)
  user.paste(text or "")

# Open the previously focused session
poppy: user.claude_open_previous_session()

# Open a session by its title
poppy {user.claude_session}: user.claude_open_session(claude_session)
