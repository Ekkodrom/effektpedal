import os
import time
import subprocess
from PyQt5.QtWidgets import QApplication
from sc3.all import Server, NetAddr  # ✅ SuperCollider Server imported here
from effect_manager import EffectManager
from gui import EffectPedalGUI
from audio_engine.audio_input import AudioInput

class MainApp:
    def __init__(self):
        self.app = QApplication([])

        # Start JACK & SuperCollider first
        self.setup_audio_system()

        # ✅ Boot SuperCollider Server BEFORE EffectManager
        print("🔹 Booting SuperCollider Server from main.py...")
        self.server = Server(name="localhost", addr=NetAddr("127.0.0.1", 57110))
        self.server.boot()
        time.sleep(4)  # Wait for server to fully start
        print("✅ SuperCollider Server Booted in main.py!")

        # ✅ Pass the shared server instance to EffectManager
        self.effect_manager = EffectManager(self.server)

        # Initialize GUI and Audio
        self.gui = EffectPedalGUI(self.effect_manager)
        self.audio = AudioInput()
        self.init_systems()

    def setup_audio_system(self):
        print("🔹 Stopping any running JACK, SuperCollider, and conflicting audio services...")
        os.system("killall -9 jackd scsynth pulseaudio pipewire wireplumber")
        time.sleep(2)

        print("🔹 Starting JACK...")
        jack_cmd = "jackd -d alsa -d hw:3,0 -r 44100 -p 1024 -n 2 &"
        subprocess.Popen(jack_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(5)

        print("🔹 Starting SuperCollider (scsynth)...")
        scsynth_cmd = "scsynth -u 57110 &"
        subprocess.Popen(scsynth_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(4)

        print("✅ Audio system initialized! JACK and SuperCollider are running.")

    def init_systems(self):
        self.audio.start()

    def run(self):
        self.gui.show()
        self.app.exec_()

if __name__ == "__main__":
    main_app = MainApp()
    main_app.run()
