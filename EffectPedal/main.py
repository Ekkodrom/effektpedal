import subprocess
import time
from PyQt5.QtWidgets import QApplication
from gui import EffectPedalGUI
from audio_engine.audio_input import AudioInput
from pythonosc import udp_client
import os

class MainApp:
    def __init__(self):
        self.start_jack()
        self.start_supercollider()
        time.sleep(2)  # Wait a bit for SuperCollider to initialize

        self.app = QApplication([])
        self.gui = EffectPedalGUI()
        self.audio = AudioInput()

    def start_jack(self):
        """Start the JACK audio server with the correct settings."""
        print("Starting JACK server...")
        jack_command = [
            "jackd", "-d", "alsa", "-d", "plughw:1,0",
            "-r", "44100", "-p", "1024", "-n", "2"
        ]
        subprocess.Popen(jack_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(3)  # Give JACK some time to start

    def start_supercollider(self):
        """Start SuperCollider server."""
        print("Starting SuperCollider...")
        scsynth_command = ["scsynth", "-u", "57110"]
        subprocess.Popen(scsynth_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def run(self):
        """Run the GUI."""
        self.gui.show()
        self.app.exec_()

if __name__ == "__main__":
    main_app = MainApp()
    main_app.run()
