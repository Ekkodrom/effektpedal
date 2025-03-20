from sc3.all import Server
from effects.granular import GranularEffect
from effects.reverb import ReverbEffect
from effects.delay import DelayEffect
from effects.revers_delay import ReverseDelayEffect
from effects.habit_granular_effect import HabitGranularEffect
from sc3.synth import Server, NetAddr  # Import NetAddr explicitly

class EffectManager:
    def __init__(self):
        print("🔹 Initializing SuperCollider Server...")
        
        # ✅ Correct way to initialize the server
        self.server = Server(name="localhost", addr=NetAddr("127.0.0.1", 57110))  # ✅ Correct!


        self.server.boot()  # Start SuperCollider
        print("✅ SuperCollider Server Booted!")

        # Pass the shared server to all effects
        self.effects = {
            "granular": GranularEffect(self.server),
            "reverb": ReverbEffect(self.server),
            "delay": DelayEffect(self.server),
            "reverse_delay": ReverseDelayEffect(self.server),
            "habit_granular": HabitGranularEffect(self.server)
        }
        self.active_effects = {}

    def start_effect(self, effect_name, **params):
        if effect_name in self.effects:
            self.active_effects[effect_name] = self.effects[effect_name]
            self.active_effects[effect_name].start_effect(**params)
            print(f"✅ {effect_name} started with params: {params}")
        else:
            print(f"❌ Effect {effect_name} not found.")

    def update_effect(self, effect_name, **params):
        if effect_name in self.active_effects:
            self.active_effects[effect_name].update_parameters(**params)
            print(f"🔄 {effect_name} updated with params: {params}")
        else:
            print(f"❌ Effect {effect_name} is not active.")

    def stop_effect(self, effect_name):
        if effect_name in self.active_effects:
            self.active_effects[effect_name].stop_effect()
            del self.active_effects[effect_name]
            print(f"🛑 {effect_name} stopped.")
        else:
            print(f"❌ Effect {effect_name} is not active.")

    def stop_all_effects(self):
        for effect_name in list(self.active_effects.keys()):
            self.stop_effect(effect_name)
        print("🚫 All effects stopped.")

if __name__ == "__main__":
    manager = EffectManager()
    manager.start_effect("granular", rate=1.2, grain_size=0.15, density=12, pan=-0.5, amp=0.7)
    manager.update_effect("granular", rate=0.8)
    manager.stop_effect("granular")
