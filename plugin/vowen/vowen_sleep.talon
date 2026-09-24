# Cancelling a dictation.
#
# The bridge disables Talon's speech recognition while Vowen records, so this
# has to live in sleep mode, and the tag keeps it from firing when Talon is
# asleep for some other reason.
#
# Vowen hears this phrase too, but a cancelled recording is discarded rather
# than transcribed, so a spoken command is fine here. Stopping is a pop
# precisely because that text is kept.
mode: sleep
and tag: user.vowen_dictating
-
(cancel dictation)$: user.vowen_dictation_cancel()
