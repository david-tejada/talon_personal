tag: user.splits
-
# Focus split
split left: user.split_last()
split right: user.split_next()

# Move splits
split move right: user.split_window_right()
split move left: user.split_window_left()
split move down: user.split_window_down()
split move up: user.split_window_up()