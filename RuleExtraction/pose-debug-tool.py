import cv2
import os
import mediapipe as mp
import numpy as np
from typing import Tuple, Dict, Any
import json

class PoseDebugTool:
    def __init__(self, video_path: str):
        """
        Initialize the debug tool with video path and MediaPipe pose detection.
        
        Args:
            video_path (str): Path to the input video file
        """
        self.video_path = video_path
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def create_landmark_video(self, frame: np.ndarray, results) -> np.ndarray:
        """
        Create a blank frame with only the pose landmarks.
        
        Args:
            frame (np.ndarray): Original video frame
            results: MediaPipe pose detection results
            
        Returns:
            np.ndarray: Frame with only landmarks drawn
        """
        # Create blank frame with white background
        h, w, _ = frame.shape
        landmark_frame = np.ones((h, w, 3), dtype=np.uint8) * 255
        
        if results.pose_landmarks:
            # Draw the pose landmarks
            self.mp_drawing.draw_landmarks(
                landmark_frame,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                self.mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
                self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2)
            )
        
        return landmark_frame

    def get_landmarks_dict(self, results) -> Dict[str, Tuple[float, float, float]]:
        """
        Convert MediaPipe landmarks to dictionary format.
        
        Args:
            results: MediaPipe pose detection results
            
        Returns:
            Dict: Dictionary containing landmark coordinates
        """
        landmarks_dict = {}
        if results.pose_landmarks:
            for idx, landmark in enumerate(results.pose_landmarks.landmark):
                landmarks_dict[f"landmark_{idx}"] = (landmark.x, landmark.y, landmark.z)
        return landmarks_dict

    def process_video(self, RuleExtraction):
        """
        Process the video and display debug information.
        Loop continues until 'n' (next) or 'q' (quit) is pressed.
        Spacebar toggles pause/play.
        
        Args:
            RuleExtraction: Function that takes landmarks and returns JSON rules
            
        Returns:
            bool: False if 'q' was pressed, True if 'n' was pressed
        """
        # Create windows for display
        cv2.namedWindow('Original Video', cv2.WINDOW_NORMAL)
        cv2.namedWindow('Pose Landmarks', cv2.WINDOW_NORMAL)
        cv2.namedWindow('Rules', cv2.WINDOW_NORMAL)
        
        paused = False
        current_frame = None
        current_landmark_frame = None
        current_rules = {}
        
        while True:  # Outer loop for video replay
            cap = cv2.VideoCapture(self.video_path)
            
            while cap.isOpened():
                if not paused:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    # Convert BGR to RGB
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    
                    # Process frame with MediaPipe
                    results = self.pose.process(frame_rgb)
                    
                    # Create landmark-only video frame
                    landmark_frame = self.create_landmark_video(frame, results)
                    
                    # Get landmarks and extract rules
                    landmarks = self.get_landmarks_dict(results)
                    rules = RuleExtraction(landmarks) if landmarks else {}
                    
                    # Store current state
                    current_frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
                    current_landmark_frame = landmark_frame
                    current_rules = rules
                
                # Create rules display
                rules_display = np.ones((480, 640, 3), dtype=np.uint8) * 255
                rules_text = json.dumps(current_rules, indent=2)
                
                # Add instructions and status to rules display
                status = "PAUSED" if paused else "PLAYING"
                instructions = [
                    f"Status: {status}",
                    "Controls:",
                    "  SPACE - Pause/Play",
                    "  n - Next video",
                    "  q - Quit"
                ]
                
                # Display instructions at the bottom
                y_pos = 420
                for instruction in instructions:
                    cv2.putText(rules_display, instruction, (10, y_pos),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
                    y_pos += 20
                
                # Display rules text
                y_pos = 30
                for line in rules_text.split('\n'):
                    cv2.putText(rules_display, line, (10, y_pos),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
                    y_pos += 20
                
                # Display all windows
                if current_frame is not None:
                    cv2.imshow('Original Video', current_frame)
                    cv2.imshow('Pose Landmarks', current_landmark_frame)
                    cv2.imshow('Rules', rules_display)
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    cap.release()
                    cv2.destroyAllWindows()
                    self.pose.close()
                    return False
                elif key == ord('n'):
                    cap.release()
                    return True
                elif key == ord(' '):  # Spacebar
                    paused = not paused
            
            if not paused:  # Only restart if not paused
                cap.release()

# Example usage:
if __name__ == "__main__":
    # Example rule extraction function (replace with actual import)
    video_folder = "../blender_mp4"
    def dummy_rule_extraction(landmarks):
        return {"sample_rule": "This is a placeholder for the actual rule extraction"}
    
    for filename in os.listdir(video_folder):
        if filename.endswith(".mp4"):
            curr_path = os.path.join(video_folder, filename)
            print(f"Processing: {filename}")  # Show which video is being processed
            debug_tool = PoseDebugTool(curr_path)
            # Continue to next video only if 'n' was pressed
            if not debug_tool.process_video(dummy_rule_extraction):
                break  # Exit if 'q' was pressed
    
    cv2.destroyAllWindows()