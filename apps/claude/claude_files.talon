app.bundle: com.anthropic.claudefordesktop
-
# These need Claude to number the files it shows, set up in ~/.claude/CLAUDE.md.
# See the top of claude_files.py.

# Open the newest file link or card numbered "[number]" in the app
view <number_small>: user.claude_open_numbered_file(number_small)

# Open the file numbered "[number]" in VS Code, in the window with its repo
edit <number_small>: user.claude_open_numbered_file_in_vscode(number_small)
