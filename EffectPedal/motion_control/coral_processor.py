import cv2
import numpy as np
import tflite_runtime.interpreter as tflite

class CoralProcessor:
    def __init__(self, model_path="movenet_singlepose_lightning.tflite"):
        self.interpreter = tflite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.cap = cv2.VideoCapture(0)  # Default camera

    def preprocess_image(self, frame):
        img = cv2.resize(frame, (192, 192))
        img = img.astype(np.float32) / 255.0
        img = np.expand_dims(img, axis=0)
        return img

    def detect_motion(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        
        input_data = self.preprocess_image(frame)
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()
        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
        keypoints = self.process_output(output_data)
        
        return keypoints
    
    def process_output(self, output_data):
        keypoints = output_data[0][0]  # Extract keypoints
        return [(kp[0], kp[1], kp[2]) for kp in keypoints]  # (x, y, confidence)

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    coral = CoralProcessor()
    try:
        while True:
            keypoints = coral.detect_motion()
            if keypoints:
                print(f"Detected keypoints: {keypoints}")
    except KeyboardInterrupt:
        coral.release()
