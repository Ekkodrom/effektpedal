from sc3.all import *
import random

class HabitGranularEffect:
    def __init__(self):
        self.server = Server(name="scsynth", addr=("127.0.0.1", 57110))  # ✅ Correct
        self.server.boot()
        self.define_habit_granular_synth()

    def define_habit_granular_synth(self):
        SynthDef("habit_granular", {
            "buf": 0,
            "rate": 1.0,
            "grain_size": 0.15,
            "density": 10,
            "pan": 0.0,
            "amp": 0.5,
            "random_pitch": 0.1,  # Random pitch deviation
            "feedback": 0.3,      # Amount of self-feedback for evolving sound
            "jitter": 0.2         # Adds randomness to grain positions
        }).add()

    def start_habit_granular(self, buf, rate=1.0, grain_size=0.15, density=10, pan=0.0, amp=0.5,
                              random_pitch=0.1, feedback=0.3, jitter=0.2):
        self.synth = Synth("habit_granular", {
            "buf": buf,
            "rate": rate,
            "grain_size": grain_size,
            "density": density,
            "pan": pan,
            "amp": amp,
            "random_pitch": random_pitch,
            "feedback": feedback,
            "jitter": jitter
        })

    def update_parameters(self, rate=None, grain_size=None, density=None, pan=None, amp=None,
                           random_pitch=None, feedback=None, jitter=None):
        if rate is not None:
            self.synth.set("rate", rate)
        if grain_size is not None:
            self.synth.set("grain_size", grain_size)
        if density is not None:
            self.synth.set("density", density)
        if pan is not None:
            self.synth.set("pan", pan)
        if amp is not None:
            self.synth.set("amp", amp)
        if random_pitch is not None:
            self.synth.set("random_pitch", random_pitch)
        if feedback is not None:
            self.synth.set("feedback", feedback)
        if jitter is not None:
            self.synth.set("jitter", jitter)

    def stop_habit_granular(self):
        self.synth.free()

if __name__ == "__main__":
    habit_granular = HabitGranularEffect()
    buf = 0  # This should be an actual buffer with an audio file or live input
    habit_granular.start_habit_granular(buf, rate=1.2, grain_size=0.15, density=12,
                                       pan=-0.5, amp=0.7, random_pitch=0.2, feedback=0.5, jitter=0.3)
