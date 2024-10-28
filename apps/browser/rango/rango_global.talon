not tag: browser
-
tab hunt <user.text>: 
  user.switcher_launch("/Applications/Brave Browser.app")
  sleep(100ms)
  user.rango_command_without_target("focusTabByText", text)

visit {user.website}:
  user.switcher_launch("/Applications/Brave Browser.app")
  sleep(100ms)
  user.rango_command_without_target("focusOrCreateTabByUrl", website)