import sounddevice as sd
import numpy as np
from queue import Queue

class AudioInput:
    def __init__(self, device=None, samplerate=44100, channels=2, buffer_size=1024):
        self.device = device  # Set to None for default device
        self.samplerate = samplerate
        self.channels = channels
        self.buffer_size = buffer_size
        self.audio_queue = Queue()
        self.stream = None

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.audio_queue.put(indata.copy())

    def start(self):
        self.stream = sd.InputStream(
            device=self.device,
            samplerate=self.samplerate,
            channels=self.channels,
            blocksize=self.buffer_size,
            callback=self.audio_callback
        )
        self.stream.start()
        print("Audio input started.")

    def get_audio_chunk(self):
        if not self.audio_queue.empty():
            return self.audio_queue.get()
        return np.zeros((self.buffer_size, self.channels))  # Return silent buffer if queue is empty

    def stop(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()
            print("Audio input stopped.")

if __name__ == "__main__":
    audio = AudioInput()
    audio.start()
    try:
        while True:
            chunk = audio.get_audio_chunk()
            print(f"Received audio chunk: {chunk.shape}")
    except KeyboardInterrupt:
        audio.stop()
