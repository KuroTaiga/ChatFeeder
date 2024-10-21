import torch
import cv2
import numpy as np
import mediapipe as mp
from collections import deque
from pathlib import Path
from yolov7.models.experimental import attempt_load  # Import this from YOLOv7 implementation
from yolov7.utils.torch_utils import select_device
from yolov7.utils.general import check_img_size,non_max_suppression

class YOLOv7EquipmentDetector:
    def __init__(self, model_path, equipment_list):
        """
        Initialize the YOLOv7 model with the provided weights and equipment list.
        :param model_path: Path to the .pt file for YOLOv7 model weights.
        :param equipment_list: List of equipment to detect (e.g., ["bench", "dumbbell", "barbell", "kettlebell", "ball"]).
        """
        #self.model = torch.hub.load('./yolov7', 'custom', path_or_model=model_path, source='local')  # Load YOLOv7 model
        self.model, self.device, self.stride, self.img_size = self.load_yolov7_model(model_path)
        self.equipment_list = equipment_list

    def load_yolov7_model(self,weights_path, img_size=640):
        if not Path(weights_path).exists:
            raise FileNotFoundError(f"Weights file not found {weights_path}")
        device = select_device('cuda' if torch.cuda.is_available() else 'cpu')  # Select device
        model = attempt_load(weights_path, map_location=device)  # Load the model onto the device
        stride = int(model.stride.max())  # Get model stride
        img_size = check_img_size(img_size, s=stride)  # Adjust image size based on model stride

        if device.type != 'cpu':
            model.half()  # Convert to half precision for better performance on GPUs

        return model, device, stride, img_size
    def detect_equipment(self, frame):
        """
        Detect equipment in a given frame.
        :param frame: A single frame from the video (numpy array).
        :return: A list of detected equipment names.
        """
        img_size = self.img_size  # Assuming the model has been loaded with this size
        resized_frame = cv2.resize(frame, (img_size, img_size)) 

        frame_tensor = torch.from_numpy(resized_frame).to(self.device).float() / 255.0  # Normalize to [0, 1]
        frame_tensor = frame_tensor.permute(2,0,1)
        if self.device.type != 'cpu':
            frame_tensor = frame_tensor.half()
        # Ensure the tensor is in the correct format (Batch size, Channels, Height, Width)
        if frame_tensor.ndimension() == 3:  # Add batch dimension if missing
            frame_tensor = frame_tensor.unsqueeze(0)
        results = self.model(frame_tensor)[0]  # Run YOLOv7 on the frame
        results = non_max_suppression(results, conf_thres=0.5,iou_thres=0.45)
        detected_equipment = []

        for detection in results:
            if len(detection):  # Check if there are any detections
                for *xyxy, conf, cls in detection:  # For each detection: bounding box coordinates (xyxy), confidence (conf), and class (cls)
                    class_idx = int(cls.item())  # Get the class index
                    confidence = conf.item()  # Get the confidence score
                    label = self.model.names[class_idx]  # Get the label from the class index
                    
                    # Only consider detections with confidence > 0.5 and if the label is in the equipment list
                    if confidence > 0.5 and label in self.equipment_list:
                        detected_equipment.append(label)  # Add the label to the detected equipment list

        return detected_equipment

class PoseDetector:
    def __init__(self, smoothing_window_size=5, spike_threshold=0.2):
        """
        Initializes the PoseDetector with optional smoothing and spike handling.
        :param smoothing_window_size: Number of frames to use for smoothing joint positions.
        :param spike_threshold: Maximum allowable difference between consecutive frames before classifying as a spike.
        """
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(static_image_mode=False, model_complexity=1, min_detection_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Window size for smoothing
        self.smoothing_window_size = smoothing_window_size
        # Threshold for detecting spikes (jumps in landmark positions)
        self.spike_threshold = spike_threshold
        
        # Maintain history of joint positions for smoothing (deque keeps a fixed-length history)
        self.joint_position_history = {
            'left_shoulder': deque(maxlen=smoothing_window_size),
            'right_shoulder': deque(maxlen=smoothing_window_size),
            'left_elbow': deque(maxlen=smoothing_window_size),
            'right_elbow': deque(maxlen=smoothing_window_size),
            'left_wrist': deque(maxlen=smoothing_window_size),
            'right_wrist': deque(maxlen=smoothing_window_size),
            'left_hip': deque(maxlen=smoothing_window_size),
            'right_hip': deque(maxlen=smoothing_window_size),
            'left_knee': deque(maxlen=smoothing_window_size),
            'right_knee': deque(maxlen=smoothing_window_size),
            'left_ankle': deque(maxlen=smoothing_window_size),
            'right_ankle': deque(maxlen=smoothing_window_size),
            'left_hand': deque(maxlen=smoothing_window_size),
            'right_hand': deque(maxlen=smoothing_window_size),
            'left_foot': deque(maxlen=smoothing_window_size),
            'right_foot': deque(maxlen=smoothing_window_size)
        }

    def _detect_pose(self, frame):
        """
        Detect pose landmarks from a given video frame using Mediapipe.
        :param frame: A single frame from the video (numpy array).
        :return: Dictionary of detected body landmarks with their positions.
        """
        # Convert the frame to RGB as Mediapipe works with RGB images
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Perform pose detection
        result = self.pose.process(frame_rgb)

        # Dictionary to store the landmark positions
        landmarks = {}

        # Extract landmark positions if detection is successful
        if result.pose_landmarks:
            for idx, landmark in enumerate(result.pose_landmarks.landmark):
                # Store landmark positions (normalized coordinates)
                landmarks[str(self.mp_pose.PoseLandmark(idx).name).lower()] = [landmark.x, landmark.y]

        return landmarks

    def smooth_landmark(self, landmark, history):
        """
        Apply smoothing to the landmark data using a moving average.
        :param landmark: Current landmark data (x, y).
        :param history: Deque containing the previous landmark positions.
        :return: Smoothed landmark data.
        """
        # Add the current position to the history
        history.append(landmark)

        # Calculate the moving average across the window
        smoothed_landmark = np.mean(history, axis=0).tolist()

        return smoothed_landmark

    def detect_spike(self, current, history):
        """
        Detect if there's a spike in the joint movement by comparing current and previous positions.
        :param current: Current landmark data (x, y).
        :param history: history of landmarks data (x, y).
        :return: Boolean indicating if a spike was detected.
        """
        if any(p is None for pose in history for p in pose):
            return False
        mean_pos = np.mean(history, axis=0)
        std_pos = np.std(history, axis=0)

        # If the current position is more than spike_threshold * standard deviation away from the mean, it's a spike
        distance_from_mean = np.abs(np.array(current) - mean_pos)
        return np.any(distance_from_mean > self.spike_threshold * std_pos)

def get_joint_positions_from_frame(self, frame):
        """
        Extract joint positions from a given frame and apply smoothing and spike detection.
        :param frame: A single frame (numpy array) from a video.
        :return: Dictionary containing joint positions for the given frame.
        """
        # Detect pose for the provided frame
        pose_landmarks = self._detect_pose(frame)

        joint_positions = {}

        # Loop through all relevant joints
        for joint, history in self.position_history.items():
            current_position = pose_landmarks.get(joint, [None, None])
            
            # Handle missing positions
            if current_position[0] is None or current_position[1] is None:
                joint_positions[joint] = self.position_hisotry.
                continue
            
            # Check if the current movement is a spike
            if len(history) > 0 and self.detect_spike(current_position, history):
                print(f"Spike detected at {joint}")
                # Keep the current position as it is, since we want to keep spikes in this case
                joint_positions[joint] = current_position
            else:
                # Apply smoothing
                smoothed_position = self.smooth_landmark(current_position, history)
                joint_positions[joint] = smoothed_position

        return joint_positions