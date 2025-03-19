from sc3.all import *

class GranularEffect:
    def __init__(self):
        self.server = Server(name="scsynth", addr=("127.0.0.1", 57110))  # ✅ Correct
        self.server.boot()
        self.define_granular_synth()

    def define_granular_synth(self):
        SynthDef("granular_synth", {
            "buf": 0,
            "rate": 1.0,
            "grain_size": 0.1,
            "density": 10,
            "pan": 0.0,
            "amp": 0.5
        }).add()

    def start_granular(self, buf, rate=1.0, grain_size=0.1, density=10, pan=0.0, amp=0.5):
        self.synth = Synth("granular_synth", {
            "buf": buf,
            "rate": rate,
            "grain_size": grain_size,
            "density": density,
            "pan": pan,
            "amp": amp
        })

    def update_parameters(self, rate=None, grain_size=None, density=None, pan=None, amp=None):
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

    def stop_granular(self):
        self.synth.free()

if __name__ == "__main__":
    granular = GranularEffect()
    buf = 0  # This should be an actual buffer with an audio file or live input
    granular.start_granular(buf, rate=1.2, grain_size=0.15, density=12, pan=-0.5, amp=0.7)
