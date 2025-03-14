import cv2
import numpy as np
from motion_control.coral_processor import CoralProcessor

class MotionTracker:
    def __init__(self, sensitivity=0.5):
        self.coral = CoralProcessor()
        self.sensitivity = sensitivity
        self.previous_positions = None

    def track_motion(self):
        keypoints = self.coral.detect_motion()
        if not keypoints:
            return None

        # Process motion
        movement = self.calculate_motion(keypoints)
        return movement
    
    def calculate_motion(self, keypoints):
        if self.previous_positions is None:
            self.previous_positions = keypoints
            return None
        
        motion_data = []
        for prev, curr in zip(self.previous_positions, keypoints):
            x_movement = abs(curr[0] - prev[0])
            y_movement = abs(curr[1] - prev[1])
            confidence = curr[2]
            
            if confidence > self.sensitivity:
                motion_data.append((x_movement, y_movement))
            else:
                motion_data.append((0, 0))
        
        self.previous_positions = keypoints
        return motion_data
    
    def release(self):
        self.coral.release()

if __name__ == "__main__":
    tracker = MotionTracker()
    try:
        while True:
            movement = tracker.track_motion()
            if movement:
                print(f"Motion detected: {movement}")
    except KeyboardInterrupt:
        tracker.release()