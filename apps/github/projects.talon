browser.host: github.com
-

drag <user.arrow_key> <user.rango_target>:
  user.rango_unhover_all()
  user.rango_focus_element(rango_target)
  key("enter {arrow_key} enter")
