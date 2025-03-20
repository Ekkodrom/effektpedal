from sc3.all import Server
from effects.granular import GranularEffect
from effects.reverb import ReverbEffect
from effects.delay import DelayEffect
from effects.revers_delay import ReverseDelayEffect
from effects.habit_granular_effect import HabitGranularEffect

# Initialize SuperCollider server here to avoid circular imports
class SuperColliderManager:
    def __init__(self):
        self.server = Server("scsynth", "127.0.0.1", 57110)

    def start(self):
        print("🔹 Starting SuperCollider...")
        self.server.boot()

# Create one instance of SuperColliderManager to be shared
sc_manager = SuperColliderManager()
sc_manager.start()

class EffectManager:
    def __init__(self):
        self.effects = {
            "granular": GranularEffect(sc_manager.server),  # Pass the shared server
            "reverb": ReverbEffect(sc_manager.server),
            "delay": DelayEffect(sc_manager.server),
            "reverse_delay": ReverseDelayEffect(sc_manager.server),
            "habit_granular": HabitGranularEffect(sc_manager.server)
        }
        self.active_effects = {}

    def start_effect(self, effect_name, **params):
        if effect_name in self.effects:
            self.active_effects[effect_name] = self.effects[effect_name]
            self.active_effects[effect_name].start_effect(**params)
            print(f"{effect_name} started with params: {params}")
        else:
            print(f"Effect {effect_name} not found.")

    def stop_effect(self, effect_name):
        if effect_name in self.active_effects:
            self.active_effects[effect_name].stop_effect()
            del self.active_effects[effect_name]
            print(f"{effect_name} stopped.")
