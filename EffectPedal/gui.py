from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QSlider, QDial, QCheckBox
from PyQt5.QtCore import Qt

class EffectPedalGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Raspberry Pi Effect Pedal")
        self.setGeometry(0, 0, 800, 480)
        
        layout = QVBoxLayout()
        
        # Effect selection
        self.effect_label = QLabel("Selected Effect: None", self)
        effect_button = QPushButton("Select Effect", self)
        effect_button.clicked.connect(self.show_effect_popup)
        
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
        layout.addWidget(effect_button)
        layout.addWidget(self.motion_control)
        layout.addWidget(self.blend_control)
        layout.addWidget(self.mixer_label)
        layout.addWidget(self.mixer_slider)
        layout.addLayout(dial_layout)
        
        self.setLayout(layout)
    
    def show_effect_popup(self):
        # Placeholder function to handle effect selection popup
        self.effect_label.setText("Selected Effect: Reverb")  # Example change
        
if __name__ == '__main__':
    app = QApplication([])
    window = EffectPedalGUI()
    window.show()
    app.exec_()
