# Start a dictation with whichever dictation software suits the focused app.
# Vowen by default, see dictation.py.
#
# The command is named for what it does rather than for a vendor, so swapping
# dictation software does not mean relearning it.
^dictate$: user.dictation_start()
