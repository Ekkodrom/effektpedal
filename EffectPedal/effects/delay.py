from sc3.all import *

class DelayEffect:
    def __init__(self):
        self.server = Server("scsynth", "127.0.0.1", 57110)  # ✅ Correct
        self.server.boot()
        self.define_delay_synth()

    def define_delay_synth(self):
        SynthDef("delay_effect", {
            "in": 0,
            "delay_time": 0.5,  # Delay time in seconds
            "feedback": 0.5,    # Controls how much of the delayed signal is fed back
            "wet": 0.5,         # Amount of delay in the mix
            "dry": 0.5,         # Amount of original signal
            "amp": 1.0
        }).add()

    def start_delay(self, in_bus=0, delay_time=0.5, feedback=0.5, wet=0.5, dry=0.5, amp=1.0):
        self.synth = Synth("delay_effect", {
            "in": in_bus,
            "delay_time": delay_time,
            "feedback": feedback,
            "wet": wet,
            "dry": dry,
            "amp": amp
        })

    def update_parameters(self, delay_time=None, feedback=None, wet=None, dry=None, amp=None):
        if delay_time is not None:
            self.synth.set("delay_time", delay_time)
        if feedback is not None:
            self.synth.set("feedback", feedback)
        if wet is not None:
            self.synth.set("wet", wet)
        if dry is not None:
            self.synth.set("dry", dry)
        if amp is not None:
            self.synth.set("amp", amp)

    def stop_delay(self):
        self.synth.free()

if __name__ == "__main__":
    delay = DelayEffect()
    delay.start_delay(delay_time=0.6, feedback=0.4, wet=0.7, dry=0.3, amp=1.2)
