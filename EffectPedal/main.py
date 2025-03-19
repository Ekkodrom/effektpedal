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
    jack_cmd = "jackd -d alsa -d hw:3,0 -r 44100 -p 1024 -n 2"
    jack_process = subprocess.Popen(jack_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Wait a bit to ensure JACK is fully initialized
    time.sleep(5)

    # Check if JACK started properly
    jack_status = subprocess.run("jack_lsp", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if jack_status.returncode != 0:
        print("❌ ERROR: JACK did not start correctly!")
        exit(1)

    print("✅ JACK is running!")

    print("🔹 Starting SuperCollider (scsynth)...")
    scsynth_cmd = "scsynth -u 57110"
    scsynth_process = subprocess.Popen(scsynth_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Wait for SuperCollider to boot
    time.sleep(3)

    # Check if SuperCollider is running
    sc_status = subprocess.run("ps aux | grep scsynth | grep -v grep", shell=True, stdout=subprocess.PIPE)
    if sc_status.stdout == b"":
        print("❌ ERROR: SuperCollider did not start correctly!")
        exit(1)

    print("✅ SuperCollider is running!")


    def init_systems(self):
        """Initialize the GUI and audio input."""
        self.audio.start()

    def run(self):
        self.gui.show()
        self.app.exec_()

if __name__ == "__main__":
    main_app = MainApp()
    main_app.run()
