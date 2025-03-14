from sc3.all import *

class ReverbEffect:
    def __init__(self):
        self.server = Server()
        self.server.boot()
        self.define_reverb_synth()

    def define_reverb_synth(self):
        SynthDef("hall_reverb", {
            "in": 0,
            "room_size": 0.8,  # Larger values create a bigger space effect
            "damping": 0.5,  # Controls how quickly high frequencies decay
            "wet": 0.5,  # Amount of reverb mixed into the signal
            "dry": 0.5,  # Amount of dry signal
            "amp": 1.0
        }).add()

    def start_reverb(self, in_bus=0, room_size=0.8, damping=0.5, wet=0.5, dry=0.5, amp=1.0):
        self.synth = Synth("hall_reverb", {
            "in": in_bus,
            "room_size": room_size,
            "damping": damping,
            "wet": wet,
            "dry": dry,
            "amp": amp
        })

    def update_parameters(self, room_size=None, damping=None, wet=None, dry=None, amp=None):
        if room_size is not None:
            self.synth.set("room_size", room_size)
        if damping is not None:
            self.synth.set("damping", damping)
        if wet is not None:
            self.synth.set("wet", wet)
        if dry is not None:
            self.synth.set("dry", dry)
        if amp is not None:
            self.synth.set("amp", amp)

    def stop_reverb(self):
        self.synth.free()

if __name__ == "__main__":
    reverb = ReverbEffect()
    reverb.start_reverb(room_size=0.9, damping=0.4, wet=0.6, dry=0.4, amp=1.2)