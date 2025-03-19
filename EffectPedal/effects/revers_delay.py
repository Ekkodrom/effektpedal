from sc3.all import *

class ReverseDelayEffect:
    def __init__(self):
        self.server = Server(name="scsynth", addr=()"127.0.0.1", 57110))  # ✅ Correct
        self.server.boot()
        self.define_reverse_delay_synth()

    def define_reverse_delay_synth(self):
        SynthDef("reverse_delay", {
            "in": 0,
            "delay_time": 0.7,    # Delay time in seconds
            "feedback": 0.5,      # Controls feedback amount
            "wet": 0.6,           # Amount of effect in mix
            "dry": 0.4,           # Amount of original signal
            "reverse_blend": 0.8, # Controls how much of the signal is reversed
            "pitch_shift": 0,     # Optional pitch shifting (-12 to +12 semitones)
            "stereo_spread": 0.5, # Controls stereo width of reversed signal
            "amp": 1.0
        }).add()

    def start_reverse_delay(self, in_bus=0, delay_time=0.7, feedback=0.5, wet=0.6, dry=0.4,
                             reverse_blend=0.8, pitch_shift=0, stereo_spread=0.5, amp=1.0):
        self.synth = Synth("reverse_delay", {
            "in": in_bus,
            "delay_time": delay_time,
            "feedback": feedback,
            "wet": wet,
            "dry": dry,
            "reverse_blend": reverse_blend,
            "pitch_shift": pitch_shift,
            "stereo_spread": stereo_spread,
            "amp": amp
        })

    def update_parameters(self, delay_time=None, feedback=None, wet=None, dry=None,
                          reverse_blend=None, pitch_shift=None, stereo_spread=None, amp=None):
        if delay_time is not None:
            self.synth.set("delay_time", delay_time)
        if feedback is not None:
            self.synth.set("feedback", feedback)
        if wet is not None:
            self.synth.set("wet", wet)
        if dry is not None:
            self.synth.set("dry", dry)
        if reverse_blend is not None:
            self.synth.set("reverse_blend", reverse_blend)
        if pitch_shift is not None:
            self.synth.set("pitch_shift", pitch_shift)
        if stereo_spread is not None:
            self.synth.set("stereo_spread", stereo_spread)
        if amp is not None:
            self.synth.set("amp", amp)

    def stop_reverse_delay(self):
        self.synth.free()

if __name__ == "__main__":
    reverse_delay = ReverseDelayEffect()
    reverse_delay.start_reverse_delay(delay_time=0.8, feedback=0.6, wet=0.7, dry=0.3,
                                      reverse_blend=0.9, pitch_shift=-3, stereo_spread=0.7, amp=1.2)
