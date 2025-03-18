from PyQt5.QtWidgets import QApplication
from gui import EffectPedalGUI
from audio_engine.audio_input import AudioInput
# from motion_control.motion_tracker import MotionTracker  # Commented out for now
from pythonosc import udp_client

osc_client = udp_client.SimpleUDPClient("127.0.0.1", 57120)  # SC listens here
osc_client.send_message("/setFreq", 440)  # send a frequency value


class MainApp:
    def __init__(self):
        self.app = QApplication([])
        self.gui = EffectPedalGUI()
        self.audio = AudioInput()
        # self.motion_tracker = MotionTracker()  # Commented out for now

        self.init_systems()

    def init_systems(self):
        # Initialize audio input
        self.audio.start()
        
        # Initialize motion tracking (commented out)
        # self.motion_tracker.start_tracking()

    def run(self):
        self.gui.show()
        self.app.exec_()

if __name__ == "__main__":
    main_app = MainApp()
    main_app.run()
