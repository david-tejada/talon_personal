# Start a Vowen dictation, even in an app whose `dictate` uses its own
# dictation (plugin/dictation). Stopping is a pop, handled in vowen.py,
# because by then the bridge has put Talon to sleep.
#
# Named for how Vowen works: it records in one go and nothing appears on
# screen until you stop.
^dictate once$: user.vowen_dictation_start()
