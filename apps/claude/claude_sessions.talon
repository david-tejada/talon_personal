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

# Open a session by the hint at the start of its title, "[A]" or "[AB]"
(slot | tab) <user.letters>: user.claude_open_session_by_hint(letters)

# Archive a session by its hint, which also removes it from the sidebar
(slot | tab) close <user.letters>: user.claude_archive_session_by_hint(letters)

# Start a new session in the open session's folder, with its settings
(slot | tab) new: key(cmd-shift-n)

# Start a new session in the folder of the session with this hint, with its settings
(slot | tab) new <user.letters>: user.claude_new_session_by_hint(letters)
