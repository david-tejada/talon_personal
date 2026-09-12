from talon import actions, app
from talon.experimental import media

_enable_speech_after_media_stops = False


def speech_enable():
    """Enable speech if it was disabled."""
    if not actions.speech.enabled():
        actions.speech.enable()


def speech_disable():
    """Disable speech if it was enabled."""
    if actions.speech.enabled():
        actions.speech.disable()


def on_media_playing(is_playing):
    """Disable or enable speech based on media playback state."""
    print("media playing", is_playing)
    global _enable_speech_after_media_stops
    if is_playing:
        _enable_speech_after_media_stops = actions.speech.enabled()
        speech_disable()
    elif _enable_speech_after_media_stops:
        speech_enable()


def on_ready():
    print("media ready")
    media.register("media_playing", on_media_playing)


app.register("ready", on_ready)
