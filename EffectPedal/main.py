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

        # 🔹 Fully stop any running JACK, SuperCollider, and conflicting audio services
        self.stop_audio_services()

        # 🔹 Start JACK & SuperCollider before initializing effects
        self.setup_audio_system()

        # ✅ Check if SuperCollider is already running
        print("🔹 Checking SuperCollider Server...")
        self.server = Server(name="localhost", addr=NetAddr("127.0.0.1", 57110))

        if self.server.is_running():
            print("✅ SuperCollider Server is already running. Connecting...")
        else:
            print("🔹 Booting SuperCollider Server from main.py...")
            self.server.boot()
            time.sleep(4)  # Wait for server to fully start
            print("✅ SuperCollider Server Booted in main.py!")

        # ✅ Pass the shared server instance to EffectManager
        self.effect_manager = EffectManager(self.server)

        # Initialize GUI and Audio
        self.gui = EffectPedalGUI(self.effect_manager)
        self.audio = AudioInput()
        self.init_systems()

    def stop_audio_services(self):
        """Kill all conflicting audio processes before starting JACK and SuperCollider."""
        print("🔹 Stopping any running JACK, SuperCollider, and conflicting audio services...")

        services = ["jackd", "scsynth", "pulseaudio", "pipewire", "wireplumber"]
        for service in services:
            subprocess.run(["killall", "-9", service], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

        time.sleep(2)  # Allow processes to properly terminate
        print("✅ All audio services stopped!")

    def setup_audio_system(self):
        """Start JACK and SuperCollider"""
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
        """Initialize Audio Input"""
        self.audio.start()

    def run(self):
        """Start the GUI"""
        self.gui.show()
        self.app.exec_()

if __name__ == "__main__":
    main_app = MainApp()
    main_app.run()
