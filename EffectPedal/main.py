import os
import time
import subprocess
from PyQt5.QtWidgets import QApplication
from gui import EffectPedalGUI
from audio_engine.audio_input import AudioInput
from pythonosc import udp_client
from sc3.all import Server

# OSC connection to SuperCollider
osc_client = udp_client.SimpleUDPClient("127.0.0.1", 57120)

class SuperColliderManager:
    def __init__(self):
        """Manages the SuperCollider server instance."""
        self.server = Server("scsynth", "127.0.0.1", 57110)
    
    def start(self):
        """Starts JACK and SuperCollider."""
        print("🔹 Stopping any running JACK, SuperCollider, and conflicting audio services...")
        os.system("killall -9 jackd scsynth pulseaudio pipewire wireplumber")
        time.sleep(2)

        print("🔹 Starting JACK...")
        jack_cmd = "jackd -d alsa -d hw:3,0 -r 44100 -p 1024 -n 2 &"
        subprocess.Popen(jack_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(5)  # Wait for JACK

        print("🔹 Starting SuperCollider (scsynth)...")
        scsynth_cmd = "scsynth -u 57110 &"
        subprocess.Popen(scsynth_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(3)  # Wait for SuperCollider to boot

        print("✅ Audio system initialized! JACK and SuperCollider are running.")
        self.server.boot()

sc_manager = SuperColliderManager()

class MainApp:
    def __init__(self):
        self.app = QApplication([])
        self.gui = EffectPedalGUI()
        self.audio = AudioInput()

        # Start JACK and SuperCollider automatically
        sc_manager.start()
        self.init_systems()

    def init_systems(self):
        """Initialize the GUI and audio input."""
        self.audio.start()

    def run(self):
        self.gui.show()
        self.app.exec_()

if __name__ == "__main__":
    main_app = MainApp()
    main_app.run()
