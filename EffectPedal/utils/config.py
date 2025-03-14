class Config:
    # Audio Settings
    SAMPLE_RATE = 44100
    BUFFER_SIZE = 1024
    AUDIO_DEVICE = None  # Set to None for default or specify device ID

    # Effect Defaults
    DEFAULT_GRAIN_SIZE = 0.1
    DEFAULT_DENSITY = 10
    DEFAULT_REVERB_ROOM = 0.8
    DEFAULT_DELAY_TIME = 0.5
    DEFAULT_FEEDBACK = 0.5
    DEFAULT_WET_DRY_MIX = 0.5

    # Motion Tracking
    MOTION_SENSITIVITY = 0.5  # Adjust for more/less responsive tracking
    CAMERA_INDEX = 0  # Default camera
    USE_CORAL = True  # Enable Coral USB Accelerator

    # SuperCollider
    SC_IP = "127.0.0.1"
    SC_PORT = 57120

    # GUI Settings
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 480

if __name__ == "__main__":
    print("Current Configuration:")
    for key, value in Config.__dict__.items():
        if not key.startswith("__"):
            print(f"{key}: {value}")