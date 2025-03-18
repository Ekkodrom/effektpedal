from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QSlider, QDial, QCheckBox, QInputDialog
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

        # Effect selection label and button
        self.effect_label = QLabel("Selected Effect: None", self)
        effect_button = QPushButton("Select Effect", self)
        effect_button.clicked.connect(self.show_effect_popup)

        # Effect control buttons (Start/Stop)
        self.start_button = QPushButton("Start Effect", self)
        self.stop_button = QPushButton("Stop Effect", self)
        self.start_button.clicked.connect(self.start_selected_effect)
        self.stop_button.clicked.connect(self.stop_selected_effect)

        # Motion control and blend toggles
        self.motion_control = QCheckBox("Cam Control", self)
        self.blend_control = QCheckBox("Blend", self)

        # Mixer section
        self.mixer_label = QLabel("Mixer Control", self)
        self.mixer_slider = QSlider(Qt.Horizontal, self)
        self.mixer_slider.setMinimum(0)
        self.mixer_slider.setMaximum(100)
        self.mixer_slider.setValue(50)

        # Circular effect controllers (dials)
        self.dials = [QDial() for _ in range(3)]
        dial_layout = QHBoxLayout()
        for dial in self.dials:
            dial.setMinimum(0)
            dial.setMaximum(100)
            dial.setValue(50)
            dial_layout.addWidget(dial)

        # Add widgets to the layout
        layout.addWidget(self.effect_label)
        layout.addWidget(effect_button)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.motion_control)
        layout.addWidget(self.blend_control)
        layout.addWidget(self.mixer_label)
        layout.addWidget(self.mixer_slider)
        layout.addLayout(dial_layout)

        self.setLayout(layout)

    def show_effect_popup(self):
        # Show a dialog to select an effect from the available options
        effects = list(self.effect_manager.effects.keys())
        effect_name, ok = QInputDialog.getItem(self, "Select Effect", "Choose an effect:", effects, 0, False)
        if ok and effect_name:
            # Store the selected effect and update the label
            self.selected_effect = effect_name
            display_name = effect_name.replace('_', ' ').title()
            self.effect_label.setText(f"Selected Effect: {display_name}")
        else:
            # If no selection was made, reset label if nothing was previously selected
            if self.selected_effect is None:
                self.effect_label.setText("Selected Effect: None")

    def start_selected_effect(self):
        # Start the currently selected effect via EffectManager
        if not self.selected_effect:
            print("No effect selected to start.")
            return
        effect_name = self.selected_effect
        if effect_name not in self.effect_manager.effects:
            print(f"Effect '{effect_name}' not recognized.")
            self.effect_label.setText("Selected Effect: None")
            self.selected_effect = None
            return
        # If the selected effect is already active, do nothing
        if effect_name in self.effect_manager.active_effects:
            print(f"Effect '{effect_name}' is already running.")
            return
        # Stop any other active effects (only one effect at a time is allowed here)
        if self.effect_manager.active_effects:
            self.effect_manager.stop_all_effects()
        # Start the selected effect
        self.effect_manager.start_effect(effect_name)
        # Update the label to indicate the effect is running
        display_name = effect_name.replace('_', ' ').title()
        self.effect_label.setText(f"Selected Effect: {display_name} (Running)")

    def stop_selected_effect(self):
        # Stop the currently selected effect via EffectManager
        if not self.selected_effect:
            print("No effect selected to stop.")
            return
        effect_name = self.selected_effect
        if effect_name not in self.effect_manager.active_effects:
            print(f"Effect '{effect_name}' is not active or already stopped.")
            return
        # Stop the effect and remove it from active effects
        self.effect_manager.stop_effect(effect_name)
        # Update the label to indicate the effect has stopped
        display_name = effect_name.replace('_', ' ').title()
        self.effect_label.setText(f"Selected Effect: {display_name} (Stopped)")

if __name__ == '__main__':
    app = QApplication([])
    window = EffectPedalGUI()
    window.show()
    app.exec_()
