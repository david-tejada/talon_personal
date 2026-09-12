# Undo/redo
redo it: edit.redo()
nope: edit.undo()

# Saving
save it: edit.save()
save all: edit.save_all()

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
cleft: key(alt-backspace)
cleft all: key(cmd-backspace)
crimp: key(alt-delete)
crimp all: key(cmd-delete)
drill: user.delete_right()

# Copy/paste
paste it: edit.paste()

# Search
find it <user.text>: edit.find(text)
