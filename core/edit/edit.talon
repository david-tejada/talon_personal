# Undo/redo
redo it: edit.redo()
nope: edit.undo()

# Saving
disk: edit.save()
disk all: edit.save_all()

# Navigation
west: edit.left()
east: edit.right()
north: edit.up()
south: edit.down()

leap: edit.word_left()
step: edit.word_right()

# Space insertion/removal
scoot: key(space left)
squash:
    edit.word_left()
    edit.delete()
    edit.word_right()

# Text removal
cleft | cliff:
  edit.extend_word_left()
  edit.delete()
(cleft | cliff) all:
  edit.extend_line_start()
  edit.delete()
crimp:
    edit.extend_word_right()
    edit.delete()
crimp all:
    edit.extend_line_end()
    edit.delete()
drill: user.delete_right()