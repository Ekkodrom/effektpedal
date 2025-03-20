import os
import time
import subprocess
from PyQt5.QtWidgets import QApplication
from sc3.all import Server, NetAddr
from effect_manager import EffectManager
from gui import EffectPedalGUI
from audio_engine.audio_input import AudioInput

class MainApp:
    def __init__(self):
        self.app = QApplication([])

        # 🔹 Stop all running JACK, SuperCollider, and conflicting audio services
        self.stop_audio_services()

        # 🔹 Start JACK & SuperCollider before initializing effects
        self.setup_audio_system()

        # ✅ Proper SuperCollider Server Handling
        self.server = self.setup_supercollider_server()

        # ✅ Pass the shared server instance to EffectManager
        self.effect_manager = EffectManager(self.server)

        # Initialize GUI and Audio
        self.gui = EffectPedalGUI(self.effect_manager)
        self.audio = AudioInput()
        self.init_systems()

    def stop_audio_services(self):
        """Kill all conflicting audio processes before starting JACK and SuperCollider."""
        print("🔹 Stopping any running JACK, SuperCollider, and conflicting audio services...")

        services = ["jackd", "scsynth", "sclang", "pulseaudio", "pipewire", "wireplumber"]
        for service in services:
            subprocess.run(["killall", "-9", service], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

        time.sleep(2)  # Allow processes to terminate

        # 🔹 Ensure port 57110 is actually free before starting SuperCollider
        while True:
            check_port_cmd = "lsof -i :57110"
            port_check = subprocess.run(check_port_cmd, shell=True, capture_output=True, text=True)

            if not port_check.stdout:
                break  # Port is free, exit loop

            print("⚠️ Port 57110 is still in use! Retrying...")
            subprocess.run(["killall", "-9", "scsynth", "sclang"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            time.sleep(2)  # Retry until the port is fully released

        print("✅ All audio services stopped and port 57110 is free!")

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

    def setup_supercollider_server(self):
        """Ensure SuperCollider server is properly set up before use"""
        print("🔹 Checking SuperCollider Server...")

        try:
            server = Server.default()
            server.addr = NetAddr("127.0.0.1", 57110)

            # ✅ Correct way to check if the server is running
            if server.status == 1:  # 1 means running
                print("✅ SuperCollider Server is already running. Connecting...")
                return server

        except Exception as e:
            print(f"⚠️ No existing SuperCollider Server found ({e}), starting a new one...")

        # 🔹 Ensure port 57110 is actually free before starting SuperCollider
        while True:
            check_port_cmd = "lsof -i :57110"
            port_check = subprocess.run(check_port_cmd, shell=True, capture_output=True, text=True)

            if not port_check.stdout:
                break  # Port is free, exit loop

            print("⚠️ Port 57110 is still in use! Retrying...")
            subprocess.run(["killall", "-9", "scsynth", "sclang"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            time.sleep(2)  # Retry until the port is fully released

        # ✅ Boot a new server with the correct addr format
        server = Server("localhost", NetAddr("127.0.0.1", 57110))
        server.boot()
        time.sleep(4)  # Wait for server to fully start
        print("✅ SuperCollider Server Booted in main.py!")

        return server

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
