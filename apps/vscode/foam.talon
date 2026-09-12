app: vscode
win.title: /notes —/
-
# Foam
today's note: user.vscode("foam-vscode.open-daily-note")
daily note: user.vscode("foam-vscode.open-daily-note-for-date")
weekly review:
  user.vscode("foam-vscode.create-note-from-template")
  sleep(400ms)
  user.paste("weekly-review.md")
  key(enter:2)

  