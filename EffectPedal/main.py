import os
import time
import subprocess
from PyQt5.QtWidgets import QApplication
from gui import EffectPedalGUI
from audio_engine.audio_input import AudioInput
from pythonosc import udp_client

# OSC connection to SuperCollider
osc_client = udp_client.SimpleUDPClient("127.0.0.1", 57120)

class MainApp:
    def __init__(self):
        self.app = QApplication([])
        self.gui = EffectPedalGUI()
        self.audio = AudioInput()

        # Start JACK and SuperCollider automatically
        self.setup_audio_system()
        self.init_systems()

    def setup_audio_system(self):
        """Stops all audio services, then starts JACK and SuperCollider correctly."""

        print("🔹 Stopping any running JACK, SuperCollider, and conflicting audio services...")
        os.system("killall -9 jackd scsynth pulseaudio pipewire wireplumber")

        # Small delay to ensure they stop
        time.sleep(2)

        print("🔹 Starting JACK...")
        jack_cmd = "jackd -d alsa -d hw:3,0 -r 44100 -p 1024 -n 2 &"
        subprocess.Popen(jack_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Wait a bit to ensure JACK is fully initialized
        time.sleep(5)

        print("🔹 Starting SuperCollider (scsynth)...")
        scsynth_cmd = "scsynth -u 57110 &"
        subprocess.Popen(scsynth_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Wait for SuperCollider to boot
        time.sleep(3)

        print("✅ Audio system initialized! JACK and SuperCollider are running.")

    def init_systems(self):
        """Initialize the GUI and audio input."""
        self.audio.start()

    def run(self):
        self.gui.show()
        self.app.exec_()

if __name__ == "__main__":
    main_app = MainApp()
    main_app.run()
