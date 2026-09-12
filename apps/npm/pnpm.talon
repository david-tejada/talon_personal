tag: terminal
-
pnpm {user.npm_command}: "pnpm {npm_command}"
pnpm add <user.text>:
  package = user.formatted_text(text, "DASH_SEPARATED")
  "pnpm add {package}"
pnpm add: "pnpm add "
pnpm add dev <user.text>:
  package = user.formatted_text(text, "DASH_SEPARATED")
  "pnpm add -D {package}"
pnpm add dev: "pnpm add -D "
