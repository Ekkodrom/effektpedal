from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout, QDial
from PyQt5.QtCore import Qt

class Mixer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        # Mixer label
        self.mixer_label = QLabel("Mixer Control", self)
        layout.addWidget(self.mixer_label)
        
        # Sliders for dry/wet mix control
        self.dry_wet_sliders = []
        self.slider_layout = QHBoxLayout()
        for i in range(4):  # Assuming 4 effects
            slider = QSlider(Qt.Vertical)
            slider.setMinimum(0)
            slider.setMaximum(100)
            slider.setValue(50)
            self.dry_wet_sliders.append(slider)
            self.slider_layout.addWidget(slider)
        layout.addLayout(self.slider_layout)
        
        # Circular dials for effect parameters
        self.dials = []
        self.dial_layout = QHBoxLayout()
        for i in range(3):  # 3 effect controllers
            dial = QDial()
            dial.setMinimum(0)
            dial.setMaximum(100)
            dial.setValue(50)
            self.dials.append(dial)
            self.dial_layout.addWidget(dial)
        layout.addLayout(self.dial_layout)
        
        self.setLayout(layout)

    def get_dry_wet_values(self):
        return [slider.value() / 100 for slider in self.dry_wet_sliders]
    
    def get_dial_values(self):
        return [dial.value() / 100 for dial in self.dials]
    
    def set_dial_values(self, values):
        for dial, value in zip(self.dials, values):
            dial.setValue(int(value * 100))

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    mixer = Mixer()
    mixer.show()
    sys.exit(app.exec_())