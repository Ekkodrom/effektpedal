from effects.granular import GranularEffect
from effects.reverb import ReverbEffect
from effects.delay import DelayEffect
from effects.revers_delay import ReverseDelayEffect
from effects.habit_granular_effect import HabitGranularEffect

class EffectManager:
    def __init__(self, server):
        print("🔹 Initializing Effect Manager...")

        # ✅ Use the already booted server from main.py
        self.server = server  

        # ✅ Pass the shared server to all effects
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
    print("⚠️ Run `main.py`, do not run `effect_manager.py` directly!")
