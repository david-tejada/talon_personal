app: warp
-
hunt all [<user.text>]:
    key(ctrl-r)
    insert(text or "")

please [<user.text>]:
    key(cmd-p)
    insert(user.text or "")

block up:
    key(cmd-up)

block down:
    key(cmd-down)

copy command:
    key(cmd-shift-c)

copy output:
    key(cmd-alt-shift-c)

split make right:
    key(cmd-d)

split make down:
    key(cmd-shift-d)

split right:
    key(cmd-alt-right)

split left:
    key(cmd-alt-left)

split up:
    key(cmd-alt-up)

split down:
    key(cmd-alt-down)

split max:
    key(cmd-shift-enter)