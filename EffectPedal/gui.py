from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QSlider, QDial, QCheckBox, QComboBox
from PyQt5.QtCore import Qt
from effect_manager import EffectManager

class EffectPedalGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.effect_manager = EffectManager()
        self.selected_effect = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Raspberry Pi Effect Pedal")
        self.setGeometry(0, 0, 800, 480)
        
        layout = QVBoxLayout()
        
        # Effect selection
        self.effect_label = QLabel("Selected Effect: None", self)
        self.effect_selector = QComboBox()
        self.effect_selector.addItems(["granular", "reverb", "delay", "reverse_delay", "habit_granular"])
        self.effect_selector.currentIndexChanged.connect(self.change_effect)
        
        # Start/Stop effect buttons
        self.effect_button = QPushButton("Start Effect", self)
        self.effect_button.clicked.connect(self.start_selected_effect)
        
        self.stop_button = QPushButton("Stop Effect", self)
        self.stop_button.clicked.connect(self.stop_selected_effect)
        
        # Motion control toggle
        self.motion_control = QCheckBox("Cam Control", self)
        self.blend_control = QCheckBox("Blend", self)
        
        # Mixer section
        self.mixer_label = QLabel("Mixer Control", self)
        self.mixer_slider = QSlider(Qt.Horizontal, self)
        self.mixer_slider.setMinimum(0)
        self.mixer_slider.setMaximum(100)
        self.mixer_slider.setValue(50)
        
        # Circular effect controllers
        self.dials = [QDial() for _ in range(3)]
        dial_layout = QHBoxLayout()
        for dial in self.dials:
            dial.setMinimum(0)
            dial.setMaximum(100)
            dial.setValue(50)
            dial_layout.addWidget(dial)
        
        # Add widgets to layout
        layout.addWidget(self.effect_label)
        layout.addWidget(self.effect_selector)
        layout.addWidget(self.effect_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.motion_control)
        layout.addWidget(self.blend_control)
        layout.addWidget(self.mixer_label)
        layout.addWidget(self.mixer_slider)
        layout.addLayout(dial_layout)
        
        self.setLayout(layout)
    
    def change_effect(self):
        self.selected_effect = self.effect_selector.currentText()
        self.effect_label.setText(f"Selected Effect: {self.selected_effect}")
    
    def start_selected_effect(self):
        if self.selected_effect:
            self.effect_manager.start_effect(self.selected_effect)
            print(f"Started effect: {self.selected_effect}")
    
    def stop_selected_effect(self):
        if self.selected_effect:
            self.effect_manager.stop_effect(self.selected_effect)
            print(f"Stopped effect: {self.selected_effect}")

if __name__ == '__main__':
    app = QApplication([])
    window = EffectPedalGUI()
    window.show()
    app.exec_()