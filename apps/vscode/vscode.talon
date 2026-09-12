app: vscode
-
# Search/open files
lisa [<user.text>] [{user.file_extension}]:
  name = text or ''
  extension = file_extension or ''
  user.vscode("workbench.action.quickOpen")
  user.paste("{name}{extension}")
poppy [<user.text>] [{user.file_extension}]:
  name = text or ''
  extension = file_extension or ''
  user.vscode("workbench.action.quickOpen")
  sleep(100ms)
  user.paste("{name}{extension}")
  sleep(100ms)
  key(enter)
poppy: user.vscode("workbench.action.openPreviousRecentlyUsedEditorInGroup")

# Search/open workspaces
pop work <user.text>:
  user.vscode("workbench.action.openRecent")
  insert(text)
  key(enter)
list work [<user.text>]:
  user.vscode("workbench.action.openRecent")
  sleep(400ms)
  insert(text or "")
pop work:
  user.vscode("workbench.action.openRecent")
  sleep(400ms)
  key(enter)

# Sidebar
side explore: user.vscode("workbench.view.explorer")
side extensions: user.vscode("workbench.view.extensions")
side outline: user.vscode("outline.focus")
side run: user.vscode("workbench.view.debug")
side search: user.vscode("workbench.view.search")
side source: user.vscode("workbench.view.scm")
side test: user.vscode("workbench.view.testing.focus")
side switch: user.vscode("workbench.action.toggleSidebarVisibility")
side tree: user.vscode("workbench.view.extension.filetree")
side database: user.vscode("workbench.view.extension.github-cweijan-mysql")
side next: key(cmd-0 down space)
side last: key(cmd-0 up space)

# Search
search again: user.vscode("rerunSearchEditorSearch")
search update:
  user.vscode("rerunSearchEditorSearch")
  edit.save()

# Symbol search
symbol hunt [<user.text>]$:
  user.vscode("workbench.action.gotoSymbol")
  sleep(50ms)
  user.insert_formatted(text or "", "NO_SPACES")

symbol hunt all [<user.text>]$:
  user.vscode("workbench.action.showAllSymbols")
  sleep(50ms)
  user.insert_formatted(text or "", "NO_SPACES")

# File
file trash:
  user.vscode("fileutils.removeFile")
  sleep(150ms)

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

# search
switch case: key(cmd-alt-c)
switch word: key(cmd-alt-w)
switch regex: key(cmd-alt-r)

# SQL
run it: user.vscode("mysql.runSQL")
run all: user.vscode("mysql.runAllQuery")
refresh it: user.vscode("mysql.template.table.update")

# Toast Notifications
toast clear: user.vscode("notifications.clearAll")

# Gitlens
review mode: user.vscode("gitlens.toggleReviewMode")
zen mode: user.vscode("gitlens.toggleZenMode")
