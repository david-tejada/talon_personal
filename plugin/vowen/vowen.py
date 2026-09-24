"""Start a Vowen dictation by voice and stop it with a pop.

The hotkey must match the toggle hotkey configured inside Vowen. It cannot be
fn, which Talon's synthetic key press does not reach.
"""

import time

from talon import Context, Module, actions, cron, settings

mod = Module()

# Plain context whose tag is toggled from Python while a dictation is active.
ctx = Context()

# Only active during a dictation, so the pop override cannot affect pops used
# anywhere else.
ctx_dictating = Context()
ctx_dictating.matches = r"""
tag: user.vowen_dictating
"""

mod.tag("vowen_dictating", desc="Active while a Vowen dictation is running")

mod.setting(
    "vowen_hotkey",
    type=str,
    default="ctrl-alt-cmd-v",
    desc="Key that toggles Vowen recording, as configured in Vowen itself",
)
mod.setting(
    "vowen_cancel_key",
    type=str,
    default="escape",
    desc="Key that discards the current recording, as configured in Vowen",
)
mod.setting(
    "vowen_stop_pops",
    type=int,
    default=2,
    desc="Pops needed to stop a dictation. Set to 1 for a single pop",
)
mod.setting(
    "vowen_double_pop_speed_maximum",
    type=float,
    default=0.4,
    desc="Longest gap in seconds accepted between two stop pops",
)
mod.setting(
    "vowen_suspend_timeout_ms",
    type=int,
    default=3000,
    desc="How long to wait for the bridge to suspend Talon before giving up",
)

_dictating = False
_suspend_seen = False
_started_monotonic = 0.0
_watch_job = None
_time_last_pop = 0.0


def _set_dictating(active: bool):
    global _dictating
    _dictating = active
    ctx.tags = ["user.vowen_dictating"] if active else []


def _speech_enabled():
    try:
        return bool(actions.speech.enabled())
    except Exception:
        return None


def _stop_watching():
    global _watch_job
    if _watch_job is not None:
        cron.cancel(_watch_job)
        _watch_job = None


def _watch():
    """Drop the tag if the recording ended by any other route.

    Vowen can also be stopped by hand, and the bridge restores Talon after its
    own failure grace period. Either way the tag must not be left stuck on, or
    it would keep swallowing pops.
    """
    global _suspend_seen

    enabled = _speech_enabled()
    if enabled is None:
        return

    if not enabled:
        # The bridge has put Talon to sleep, so the recording really started.
        _suspend_seen = True
        return

    if _suspend_seen:
        # Talon is listening again, so the recording is over.
        _stop_watching()
        _set_dictating(False)
        return

    if time.monotonic() - _started_monotonic > settings.get(
        "user.vowen_suspend_timeout_ms"
    ) / 1000.0:
        # The bridge never suspended Talon, so assume nothing is recording.
        _stop_watching()
        _set_dictating(False)


@mod.action_class
class Actions:
    def vowen_dictation_start():
        """Toggle Vowen recording on and arm the pop that stops it."""
        global _suspend_seen, _started_monotonic, _watch_job, _time_last_pop

        if _dictating:
            return

        actions.key(settings.get("user.vowen_hotkey"))

        _suspend_seen = False
        _started_monotonic = time.monotonic()
        _time_last_pop = 0.0
        _set_dictating(True)

        _stop_watching()
        _watch_job = cron.interval("100ms", _watch)

    def vowen_dictation_stop():
        """Toggle Vowen recording off."""
        if not _dictating:
            return

        actions.key(settings.get("user.vowen_hotkey"))
        _stop_watching()
        _set_dictating(False)

    def vowen_dictation_cancel():
        """Discard the current recording instead of transcribing it."""
        if not _dictating:
            return

        actions.key(settings.get("user.vowen_cancel_key"))
        _stop_watching()
        _set_dictating(False)


@ctx_dictating.action_class("user")
class DictatingActions:
    def noise_trigger_pop():
        global _time_last_pop

        if settings.get("user.vowen_stop_pops") < 2:
            actions.user.vowen_dictation_stop()
            return

        # Two pops close together. There is deliberately no minimum gap: an
        # earlier version rejected pops for being too fast as well as too
        # slow, which made it hard to trigger at all.
        now = time.perf_counter()
        delta = now - _time_last_pop
        _time_last_pop = now

        if delta <= settings.get("user.vowen_double_pop_speed_maximum"):
            actions.user.vowen_dictation_stop()
