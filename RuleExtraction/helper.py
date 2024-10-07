# math_helper.py
import os
import mediapipe as mp
import math
import cv2
from typing import Tuple

def calculate_angle(a: Tuple[float, float], b: Tuple[float, float], c: Tuple[float, float]) -> float:
    """
    Calculates the angle formed at point b by the line segments ba and bc.

    Args:
        a (Tuple[float, float]): Coordinates of point a (x, y).
        b (Tuple[float, float]): Coordinates of point b (x, y).
        c (Tuple[float, float]): Coordinates of point c (x, y).

    Returns:
        float: The angle in degrees between the lines ba and bc at point b.
    """
    # Calculate the angle using the arctangent of the determinant and dot product
    ab = (a[0] - b[0], a[1] - b[1])
    cb = (c[0] - b[0], c[1] - b[1])
    dot_product = ab[0] * cb[0] + ab[1] * cb[1]
    determinant = ab[0] * cb[1] - ab[1] * cb[0]
    angle = math.degrees(math.atan2(determinant, dot_product))
    angle = angle + 360 if angle < 0 else angle
    return angle

def calculate_distance(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    """
    Calculates the Euclidean distance between two points.

    Args:
        a (Tuple[float, float]): Coordinates of point a (x, y).
        b (Tuple[float, float]): Coordinates of point b (x, y).

    Returns:
        float: The distance between points a and b.
    """
    return math.hypot(a[0] - b[0], a[1] - b[1])

def get_joint_positions_from_video_old(video_path):
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
    cap = cv2.VideoCapture(video_path)
    joint_positions_over_time = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results_pose = pose.process(image)
        if results_pose.pose_landmarks:
            landmarks = results_pose.pose_landmarks.landmark
            joint_positions = {
                'left_shoulder': (landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                  landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y),
                'right_shoulder': (landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                   landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y),
                'left_elbow': (landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                               landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y),
                'right_elbow': (landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                                landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y),
                'left_wrist': (landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                               landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y),
                'right_wrist': (landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                                landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y),
                'left_hip': (landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y),
                'right_hip': (landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y),
                'left_knee': (landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y),
                'right_knee': (landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                               landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y),
                'left_ankle': (landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                               landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y),
                'right_ankle': (landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                                landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y),
                # 'nose': (landmarks[mp_pose.PoseLandmark.NOSE.value].x,
                        #  landmarks[mp_pose.PoseLandmark.NOSE.value].y),
                'left_foot': (landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].y),
                'right_foot': (landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].x,
                               landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].y),
                'left_hand': (landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].y),
                'right_hand': (landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value].x,
                               landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value].y),

                # 'back': (

                #     (landmarks[mp_pose.PoseLandmark.NOSE.value].x +

                #      landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x +

                #      landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x) / 3,

                #     (landmarks[mp_pose.PoseLandmark.NOSE.value].y +

                #      landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y +

                #      landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y) / 3

                # )
            }
            joint_positions_over_time.append(joint_positions)

    

    cap.release()

    return joint_positions_over_time

def get_empty_landmarks():
    return {
        "left_foot": {"position": [], "motion": []},
        "right_foot": {"position": [], "motion": []},
        "left_hip": {"position": [], "motion": []},
        "right_hip": {"position": [], "motion": []},
        "torso": {"position": [], "motion": []},
        "left_hand": {"position": [], "motion": []},
        "right_hand": {"position": [], "motion": []},
        "left_elbow": {"position": [], "motion": []},
        "right_elbow": {"position": [], "motion": []},
        "left_shoulder": {"position": [], "motion": []},
        "right_shoulder": {"position": [], "motion": []},
        "left_knee": {"position": [], "motion": []},
        "right_knee": {"position": [], "motion": []}
    }
def get_torso_landmarks():
    return {
        "torso": {"position": [], "motion": []},
        "left_hip": {"position": [], "motion": []},
        "right_hip": {"position": [], "motion": []},
        "left_shoulder": {"position": [], "motion": []},
        "right_shoulder": {"position": [], "motion": []}
    }
def get_arm_landmarks():
    return {
        "left_elbow": {"position": [], "motion": []},
        "right_elbow": {"position": [], "motion": []},
        "left_wrist": {"position": [], "motion": []},
        "right_wrist": {"position": [], "motion": []},
        "left_hand": {"position": [], "motion": []},
        "right_hand": {"position": [], "motion": []}
    }
def get_leg_landmarks():
    return {
        "left_knee": {"position": [], "motion": []},
        "right_knee": {"position": [], "motion": []},
        "left_ankle": {"position": [], "motion": []},
        "right_ankle": {"position": [], "motion": []},
        "left_foot": {"position": [], "motion": []},
        "right_foot": {"position": [], "motion": []}
    }
def get_empty_motion():
    return {
        "left_foot": {"motion": []},
        "right_foot": {"motion": []},
        "left_hip": {"motion": []},
        "right_hip": {"motion": []},
        "torso": {"motion": []},
        "left_hand": {"motion": []},
        "right_hand": {"motion": []},
        "left_elbow": {"motion": []},
        "right_elbow": {"motion": []},
        "left_shoulder": {"motion": []},
        "right_shoulder": {"motion": []},
        "left_knee": {"motion": []},
        "right_knee": {"motion": []}
    }

def get_empty_torso_motion():
    return {
        "torso": {"motion": []},
        "left_hip": {"motion": []},
        "right_hip": {"motion": []},
        "left_shoulder": {"motion": []},
        "right_shoulder": {"motion": []},
    }
def get_empty_arm_motion():
    return {
        "left_elbow": {"motion": []},
        "right_elbow": {"motion": []},
        "left_wrist": {"motion": []},
        "right_wrist": {"motion": []},
        "left_hand": {"motion": []},
        "right_hand": {"motion": []}
    }
def get_empty_leg_motion():
    return {
        "left_knee": {"motion": []},
        "right_knee": {"motion": []},
        "left_ankle": {"motion": []},
        "right_ankle": {"motion": []},
        "left_foot": {"motion": []},
        "right_foot": {"motion": []}
    }
def get_empty_position():
    return {
        "left_foot": {"position": []},
        "right_foot": {"position": []},
        "left_hip": {"position": []},
        "right_hip": {"position": []},
        "torso": {"position": []},
        "left_hand": {"position": []},
        "right_hand": {"position": []},
        "left_elbow": {"position": []},
        "right_elbow": {"position": []},
        "left_shoulder": {"position": []},
        "right_shoulder": {"position": []},
        "left_knee": {"position": []},
        "right_knee": {"position": []}
    }

def get_empty_torso_position():
    return {
        "torso": {"position": []},
        "left_hip": {"position": []},
        "right_hip": {"position": []},
        "left_shoulder": {"position": []},
        "right_shoulder": {"position": []},
    }
def get_empty_arm_position():
    return {
        "left_elbow": {"position": []},
        "right_elbow": {"position": []},
        "left_wrist": {"position": []},
        "right_wrist": {"position": []},
        "left_hand": {"position": []},
        "right_hand": {"position": []}
    }

def get_empty_leg_position():
    return {
        "left_knee": {"position": []},
        "right_knee": {"position": []},
        "left_ankle": {"position": []},
        "right_ankle": {"position": []},
        "left_foot": {"position": []},
        "right_foot": {"position": []}
    }


def calculate_match(actual,expected):
    return 0

def get_video_path(root_dir: str, target: list)->tuple:
    video_result = []
    exercise_result = []
    for dirpath,_,filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".mp4"):
                curr = os.path.splitext(filename)[0].lower()
                if curr in target:
                    exercise_result.append(curr)
                    video_result.append(os.path.join(dirpath,filename))
                else:
                    print(f"video name not found in exercise: {curr}")
    return video_result,exercise_result

def build_rule_dict(rules):
    body_landmarks_dict = {}
    equipment_dict = {}
    other_dict = {}
    # Iterate through the list of exercise rules
    for rule in rules:
        activity_name = rule.get("activity", "").strip()

        if activity_name:  # Ensure the activity name is not empty
            body_landmarks_dict[activity_name] = rule.get("body_landmarks", {})
            equipment_dict[activity_name] = rule.get("equipment", {})
            other_dict[activity_name] = rule.get("other",{})
    return body_landmarks_dict, equipment_dict, other_dict

