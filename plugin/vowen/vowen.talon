# Start a dictation. Stopping is a pop, handled in vowen.py, because by then
# the bridge has put Talon to sleep.
#
# The command is named for what it does rather than for Vowen, so swapping
# dictation software does not mean relearning it.
^dictate$: user.vowen_dictation_start()
