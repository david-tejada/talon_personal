app.bundle: com.anthropic.claudefordesktop
-
# These need Claude to number its links, set up in ~/.claude/CLAUDE.md.
# See the top of claude_files.py.

# Open the link numbered "[number]": a file in VS Code, a web page in the
# default browser
follow <number_small>: user.claude_follow_numbered_link(number_small)
