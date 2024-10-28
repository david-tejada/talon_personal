app: vscode
-
# Search/open files
lisa [<user.text>] [{user.file_extension}]:
  user.vscode("workbench.action.quickOpen")
  sleep(400ms)
  insert(text or "")
  insert(file_extension or "")
  sleep(300ms)
poppy <user.text> [{user.file_extension}]:
  user.vscode("workbench.action.quickOpen")
  sleep(400ms)
  insert(text or "")
  insert(file_extension or "")
  sleep(400ms)
  key(enter)
  sleep(150ms)
poppy: user.vscode("workbench.action.openPreviousRecentlyUsedEditorInGroup")

# Search/open workspaces
pop work <user.text>:
  user.vscode("workbench.action.openRecent")
  sleep(400ms)
  insert(text)
  sleep(300ms)
  key(enter)
  sleep(150ms)
list work [<user.text>]:
  user.vscode("workbench.action.openRecent")
  sleep(400ms)
  insert(text or "")
pop work:
  user.vscode("workbench.action.openRecent")
  sleep(400ms)
  key(enter)

# Git
file revert: user.vscode("workbench.action.files.revert")
git clean: user.vscode("git.clean")
git open: user.vscode("git.openFile")

# Live server
go live: user.vscode("extension.liveServer.goOnline")

# Markdown Preview
side preview: user.vscode("markdown.showPreviewToSide")
preview refresh: user.vscode("markdown.preview.refresh")

# Andreas-talon
generate range [from <number_small>]:
    user.run_rpc_command("andreas.generateRange", number_small or 1)

bar next: key(cmd-0 down space)
bar last: key(cmd-0 up space)

# search
switch case: key(cmd-alt-c)
switch word: key(cmd-alt-w)
switch regex: key(cmd-alt-r)

# Codeium
suggest: key(alt-\)
next comp: key(alt-])
next comp: key(alt-[)
codeium command: key(cmd-shift-i)
codeium accept: key(alt-a)
codeium switch: user.vscode("codeium.toggleAutocompleteForCurrentLanguage")