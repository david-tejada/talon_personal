app.bundle: com.anthropic.claudefordesktop
-
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
