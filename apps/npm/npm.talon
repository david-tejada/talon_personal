tag: terminal
-
node {user.npm_command}: "npm {npm_command}"
node install <user.text>:
  package = user.formatted_text(text, "DASH_SEPARATED")
  "npm install {package}"
node run <user.text>:
  command = user.formatted_text(text, "DASH_SEPARATED")
  "npm run {command}"
