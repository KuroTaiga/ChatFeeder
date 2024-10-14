import torch
import cv2
import mediapipe as mp
from pathlib import Path
from yolov7.models.experimental import attempt_load  # Import this from YOLOv7 implementation
from yolov7.utils.torch_utils import select_device
from yolov7.utils.general import check_img_size

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

        detected_equipment = []

        for detection in results:
            # x1, y1, x2, y2 = detection[0].item(), detection[1].item(), detection[2].item(), detection[3].item()
            confidence = detection[4].item()
            class_idx = int(detection[5].item())  # Convert class index to int

            label = self.model.names[int(class_idx)]  # Convert class index to class label
            if label in self.equipment_list and confidence > 0.5:  # Check confidence threshold
                detected_equipment.append(label)

        return detected_equipment

class PoseDetector:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(static_image_mode=False, model_complexity=1, min_detection_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils

    def detect_pose(self, frame):
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
                landmarks[self.mp_pose.PoseLandmark(idx).name] = {
                    'x': landmark.x,
                    'y': landmark.y,
                    'z': landmark.z
                }

        return landmarks

    def get_joint_positions_from_frame(self, frame):
        """
        Extract joint positions from a given frame.
        :param frame: A single frame (numpy array) from a video.
        :return: Dictionary containing joint positions for the given frame.
        """
        # Detect pose for the provided frame
        pose_landmarks = self.detect_pose(frame)

        joint_positions = {
            'left_shoulder': pose_landmarks.get('LEFT_SHOULDER', {'x': None, 'y': None}),
            'right_shoulder': pose_landmarks.get('RIGHT_SHOULDER', {'x': None, 'y': None}),
            'left_elbow': pose_landmarks.get('LEFT_ELBOW', {'x': None, 'y': None}),
            'right_elbow': pose_landmarks.get('RIGHT_ELBOW', {'x': None, 'y': None}),
            'left_wrist': pose_landmarks.get('LEFT_WRIST', {'x': None, 'y': None}),
            'right_wrist': pose_landmarks.get('RIGHT_WRIST', {'x': None, 'y': None}),
            'left_hip': pose_landmarks.get('LEFT_HIP', {'x': None, 'y': None}),
            'right_hip': pose_landmarks.get('RIGHT_HIP', {'x': None, 'y': None}),
            'left_knee': pose_landmarks.get('LEFT_KNEE', {'x': None, 'y': None}),
            'right_knee': pose_landmarks.get('RIGHT_KNEE', {'x': None, 'y': None}),
            'left_ankle': pose_landmarks.get('LEFT_ANKLE', {'x': None, 'y': None}),
            'right_ankle': pose_landmarks.get('RIGHT_ANKLE', {'x': None, 'y': None}),
            'left_hand': pose_landmarks.get('LEFT_INDEX', {'x': None, 'y': None}),
            'right_hand': pose_landmarks.get('RIGHT_INDEX', {'x': None, 'y': None}),
            'left_foot': pose_landmarks.get('LEFT_HEEL', {'x': None, 'y': None}),
            'right_foot': pose_landmarks.get('RIGHT_HEEL', {'x': None, 'y': None}),
        }

        return joint_positions
