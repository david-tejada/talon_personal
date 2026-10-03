app.bundle: com.anthropic.claudefordesktop
-
# Sessions

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

# Links

# Open the link numbered "[number]": a file in VS Code, a web page in the
# default browser. This needs Claude to number its links, set up in
# ~/.claude/CLAUDE.md. See "Numbered links" in claude.py.
follow <number_small>: user.claude_follow_numbered_link(number_small)

# Scrolling

# Scroll the chat by two thirds of its height, like Rango does in the browser
upper: user.claude_scroll("chat", "up")
downer: user.claude_scroll("chat", "down")

# Scroll by a number of chat heights
upper <number_small>: user.claude_scroll("chat", "up", number_small)
downer <number_small>: user.claude_scroll("chat", "down", number_small)

# Scroll to the top or bottom of the chat
upper all: user.claude_scroll("chat", "up", 9999)
downer all: user.claude_scroll("chat", "down", 9999)

tiny up: user.claude_scroll("chat", "up", 0.2)
tiny down: user.claude_scroll("chat", "down", 0.2)

# The same for the file open in the file pane
upper file: user.claude_scroll("file", "up")
downer file: user.claude_scroll("file", "down")
upper file <number_small>: user.claude_scroll("file", "up", number_small)
downer file <number_small>: user.claude_scroll("file", "down", number_small)
upper file all: user.claude_scroll("file", "up", 9999)
downer file all: user.claude_scroll("file", "down", 9999)
tiny up file: user.claude_scroll("file", "up", 0.2)
tiny down file: user.claude_scroll("file", "down", 0.2)

# Prompt

# Put the cursor back in the prompt box, for when focus gets lost, for
# example after cancelling dictation
focus chat: user.claude_focus_prompt()

# Records with the Claude app's own mic. Bare `dictate` still starts Vowen
# here (plugin/vowen/vowen.talon), so either one is available.
^claude dictate$: user.claude_dictate_start()
