import cv2
import mediapipe as mp
import math
import json
import numpy as np
import pandas as pd
import os
import torch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
from pathlib import Path
import sys
import subprocess  # Added to call detect_revise.py

# Initialize Mediapipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Load YOLOv7 model
def load_yolov7_model(weights_path, img_size=640):
    device = select_device('cuda' if torch.cuda.is_available() else 'cpu')
    model = attempt_load(weights_path, map_location=device)  # Load model
    stride = int(model.stride.max())  # Get model stride
    img_size = check_img_size(img_size, s=stride)  # Check image size
    if device.type != 'cpu':
        model.half()  # Convert model to half precision if using GPU
    return model, device, stride, img_size

# Perform equipment detection by calling detect_revise.py
def detect_equipment_via_script(detect_script_path, weights_path, video_path, conf_threshold=0.25, img_size=640):
    """
    Calls the detect_revise.py script as a subprocess and captures the detected equipment string.
    """
    cmd = [
        'python',
        detect_script_path,
        '--weights', weights_path,
        '--source', video_path,
        '--conf-thres', str(conf_threshold),
        '--img-size', str(img_size),
        '--nosave'  # Add any other flags as needed
    ]
    
    try:
        # Run the detect_revise.py script and capture the output
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        stdout = result.stdout
        stderr = result.stderr
        
        if stderr:
            print(f"Error during equipment detection for {video_path}:\n{stderr}")
        
        # Parse the equipment string from stdout
        # Assuming the script prints "=== Final Detected Equipment ===" followed by the equipment string
        equipment_str = "none"
        lines = stdout.split('\n')
        for i, line in enumerate(lines):
            if "=== Final Detected Equipment ===" in line:
                if i + 1 < len(lines):
                    equipment_dict_str = lines[i + 1].strip()
                    try:
                        equipment_dict = eval(equipment_dict_str)  # Convert string dict to actual dict
                        if equipment_dict:
                            equipment_str = max(equipment_dict, key=equipment_dict.get)
                        else:
                            equipment_str = "none"
                    except:
                        equipment_str = "none"
                break
        return equipment_str
    except subprocess.CalledProcessError as e:
        print(f"Failed to run detect_revise.py for {video_path}. Error: {e}")
        return "none"

# Build exercise rules with equipment and detailed features
def build_exercise_rules_json():
    # Define exercise rules in JSON format with features as strings
    exercise_rules = {
        "Abdominals Stretch": {
            "posture": "lying_flat",
            "arm": "arms_overhead",
            "leg": "extended",
            "equipment": "none",
            "elbow_angle": "extended",
            "knee_angle": "straight"
        },
        # ... (other exercises omitted for brevity)
        "Renegade Row": {
            "posture": "plank",
            "arm": "rowing",
            "leg": "shoulder_width_apart",
            "equipment": "Dumbbell",
            "elbow_angle": "bent",
            "knee_angle": "straight"
        }
    }
    return exercise_rules

# Calculate Jaccard similarity (Not used in this integration but kept for reference)
def jaccard_similarity(set1, set2):
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    if not union:
        return 0
    return len(intersection) / len(union)

# Get joint positions from video
def get_joint_positions_from_video(video_path, pose):
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
                'nose': (landmarks[mp_pose.PoseLandmark.NOSE.value].x,
                         landmarks[mp_pose.PoseLandmark.NOSE.value].y),
                'left_foot': (landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].y),
                'right_foot': (landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].x,
                               landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].y),
                'left_hand': (landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].y),
                'right_hand': (landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value].x,
                               landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value].y),
                'back': (
                    (landmarks[mp_pose.PoseLandmark.NOSE.value].x +
                     landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x +
                     landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x) / 3,
                    (landmarks[mp_pose.PoseLandmark.NOSE.value].y +
                     landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y +
                     landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y) / 3
                )
            }
            joint_positions_over_time.append(joint_positions)
    
    cap.release()
    return joint_positions_over_time

# Aggregate equipment detections using majority voting
def aggregate_equipment_detections(equipment_over_time):
    equipment_counts = defaultdict(int)
    
    for frame_equipment in equipment_over_time:
        equipment_counts[frame_equipment] += 1
    
    if not equipment_counts:
        return "none"
    
    # Select the equipment with the highest count
    sorted_equipment = sorted(equipment_counts.items(), key=lambda x: x[1], reverse=True)
    top_equipment = sorted_equipment[0][0]
    
    return top_equipment

# Generate joint features including equipment and additional details
def generate_joint_features(joint_positions, equipment):
    features = {
        "posture": "",
        "arm": "",
        "leg": "",
        "equipment": equipment,
        "elbow_angle": "",
        "knee_angle": ""
    }

    # Posture
    left_shoulder_y = joint_positions['left_shoulder'][1]
    right_shoulder_y = joint_positions['right_shoulder'][1]
    left_hip_y = joint_positions['left_hip'][1]
    right_hip_y = joint_positions['right_hip'][1]
    back_y = joint_positions['back'][1]

    avg_shoulder_y = (left_shoulder_y + right_shoulder_y) / 2
    avg_hip_y = (left_hip_y + right_hip_y) / 2

    if abs(avg_shoulder_y - avg_hip_y) < 0.05:
        features["posture"] = "standing"
    elif abs(avg_shoulder_y - back_y) < 0.04:
        features["posture"] = "upright"
    elif (abs(avg_shoulder_y - back_y) >= 0.04 and
          abs(avg_shoulder_y - avg_hip_y) >= 0.05 and
          avg_hip_y > min(joint_positions['left_knee'][1], joint_positions['right_knee'][1])):
        features["posture"] = "seated"
    else:
        features["posture"] = "bent"

    # Legs
    left_knee_y = joint_positions['left_knee'][1]
    right_knee_y = joint_positions['right_knee'][1]
    left_hip_y = joint_positions['left_hip'][1]
    right_hip_y = joint_positions['right_hip'][1]
    left_foot_y = joint_positions['left_foot'][1]
    right_foot_y = joint_positions['right_foot'][1]

    avg_knee_y = (left_knee_y + right_knee_y) / 2
    avg_hip_y = (left_hip_y + right_hip_y) / 2

    if avg_knee_y < avg_hip_y:
        features["leg"] = "bent"
    elif abs(joint_positions['left_knee'][0] - joint_positions['right_knee'][0]) > 0.1:
        features["leg"] = "staggered"
    else:
        features["leg"] = "shoulder_width_apart"

    # Leg extension
    if left_foot_y > left_knee_y or right_foot_y > right_knee_y:
        features["leg"] = "extended"
    elif features["leg"] != "staggered":
        features["leg"] = "calf_raise"

    # Arm position
    left_wrist_x, left_wrist_y = joint_positions['left_wrist']
    right_wrist_x, right_wrist_y = joint_positions['right_wrist']
    left_shoulder_y = joint_positions['left_shoulder'][1]
    right_shoulder_y = joint_positions['right_shoulder'][1]

    if abs(left_wrist_x - right_wrist_x) > 0.2:
        features["arm"] = "extended"
    elif left_wrist_y < joint_positions['left_shoulder'][1] and right_wrist_y < joint_positions['right_shoulder'][1]:
        features["arm"] = "arms_overhead"
    else:
        features["arm"] = "arms_bent"

    # Add more features to improve accuracy
    # For example, calculate angles of arms and legs
    def calculate_angle(a, b, c):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)
        if angle > 180.0:
            angle = 360 - angle
        return angle

    # Calculate left elbow angle
    left_elbow_angle = calculate_angle(
        joint_positions['left_shoulder'],
        joint_positions['left_elbow'],
        joint_positions['left_wrist']
    )
    # Calculate right elbow angle
    right_elbow_angle = calculate_angle(
        joint_positions['right_shoulder'],
        joint_positions['right_elbow'],
        joint_positions['right_wrist']
    )

    # Calculate left knee angle
    left_knee_angle = calculate_angle(
        joint_positions['left_hip'],
        joint_positions['left_knee'],
        joint_positions['left_ankle']
    )
    # Calculate right knee angle
    right_knee_angle = calculate_angle(
        joint_positions['right_hip'],
        joint_positions['right_knee'],
        joint_positions['right_ankle']
    )

    # Refine arm features based on elbow angles
    avg_elbow_angle = (left_elbow_angle + right_elbow_angle) / 2
    if avg_elbow_angle > 160:
        features["arm"] = "extended"
        features["elbow_angle"] = "extended"
    elif avg_elbow_angle < 90:
        features["arm"] = "bent"
        features["elbow_angle"] = "bent"
    else:
        features["arm"] = "half_bent"
        features["elbow_angle"] = "half_bent"

    # Refine leg features based on knee angles
    avg_knee_angle = (left_knee_angle + right_knee_angle) / 2
    if avg_knee_angle > 160:
        features["knee_angle"] = "straight"
    elif avg_knee_angle < 90:
        features["knee_angle"] = "bent"
    else:
        features["knee_angle"] = "half_bent"

    return features

# Process exercise and calculate similarity
def process_exercise(video_path, exercise_rules, vectorizer, exercise_names, detect_script_path, yolov7_weights_path, conf_threshold=0.25, img_size=640):
    # Detect equipment by calling detect_revise.py
    detected_equipment = detect_equipment_via_script(
        detect_script_path=detect_script_path,
        weights_path=yolov7_weights_path,
        video_path=video_path,
        conf_threshold=conf_threshold,
        img_size=img_size
    )
    
    # Get joint positions
    joint_positions_over_time = get_joint_positions_from_video(video_path, pose)
    
    if not joint_positions_over_time:
        print(f"No joint positions detected in {video_path}.")
        return [("none", 0.0)] * 3  # Return dummy values
    
    # Generate joint features with equipment
    video_features_over_time = [generate_joint_features(jp, detected_equipment) for jp in joint_positions_over_time]
    
    # Generate aggregated features
    video_features = {
        "posture": [],
        "arm": [],
        "leg": [],
        "equipment": [],
        "elbow_angle": [],
        "knee_angle": []
    }
    for features in video_features_over_time:
        video_features["posture"].append(features["posture"])
        video_features["arm"].append(features["arm"])
        video_features["leg"].append(features["leg"])
        video_features["equipment"].append(features["equipment"])
        video_features["elbow_angle"].append(features["elbow_angle"])
        video_features["knee_angle"].append(features["knee_angle"])
    
    # Select the most frequent feature
    aggregated_features = {
        "posture": max(set(video_features["posture"]), key=video_features["posture"].count) if video_features["posture"] else "",
        "arm": max(set(video_features["arm"]), key=video_features["arm"].count) if video_features["arm"] else "",
        "leg": max(set(video_features["leg"]), key=video_features["leg"].count) if video_features["leg"] else "",
        "equipment": max(set(video_features["equipment"]), key=video_features["equipment"].count) if video_features["equipment"] else "none",
        "elbow_angle": max(set(video_features["elbow_angle"]), key=video_features["elbow_angle"].count) if video_features["elbow_angle"] else "",
        "knee_angle": max(set(video_features["knee_angle"]), key=video_features["knee_angle"].count) if video_features["knee_angle"] else ""
    }
    
    # Convert features to string, including equipment and angles
    video_text = f'posture:{aggregated_features["posture"]} arm:{aggregated_features["arm"]} leg:{aggregated_features["leg"]} equipment:{aggregated_features["equipment"]} elbow_angle:{aggregated_features["elbow_angle"]} knee_angle:{aggregated_features["knee_angle"]}'
    
    # Build exercise rules as strings, including equipment and angles
    exercise_texts = []
    for exercise, features in exercise_rules.items():
        text = f'posture:{features["posture"]} arm:{features["arm"]} leg:{features["leg"]} equipment:{features["equipment"]} elbow_angle:{features["elbow_angle"]} knee_angle:{features["knee_angle"]}'
        exercise_texts.append(text)
    
    # Vectorize
    corpus = exercise_texts + [video_text]
    tfidf_matrix = vectorizer.fit_transform(corpus)
    exercise_vectors = tfidf_matrix[:-1]
    video_vector = tfidf_matrix[-1]
    
    # Calculate cosine similarity
    similarities = cosine_similarity(video_vector, exercise_vectors)[0]
    
    # Get top 3 exercises
    top_indices = similarities.argsort()[-3:][::-1]
    top_three = [(exercise_names[i], similarities[i]*100) for i in top_indices]
    
    return top_three

# Collect video files, focusing only on specified exercises
def collect_video_files(root_dir, allowed_exercises):
    video_files = []
    exercise_names = []
    for folder_num in range(1, 48):  # Changed to 47 to include folder_47 if exists
        folder_name = f"folder_{folder_num}"
        folder_path = os.path.join(root_dir, folder_name)
        if not os.path.isdir(folder_path):
            continue
        for file in os.listdir(folder_path):
            if file.endswith(".mp4"):
                exercise_name = os.path.splitext(file)[0]
                if exercise_name in allowed_exercises:
                    video_path = os.path.join(folder_path, file)
                    video_files.append(video_path)
                    exercise_names.append(exercise_name)
    return video_files, exercise_names

# Main processing flow
def main():
    exercise_rules = build_exercise_rules_json()
    exercise_names = list(exercise_rules.keys())
    
    # Define equipment categories for YOLOv7 detection
    equipment_classes = ["Ball", "Barbell", "Dumbbell", "Kettlebell"]  # Removed 'Band'
    

    
    # Collect video files
    video_files, actual_exercises = collect_video_files(video_root_dir, exercise_names)
    
    if not video_files:
        print("No matching .mp4 video files found. Please check if the video file names match the predefined exercise names.")
        return
    
    results = []
    
    # Initialize vectorizer
    vectorizer = TfidfVectorizer()
    
    for video_path, actual_exercise in zip(video_files, actual_exercises):
        print(f"Processing video: {video_path}")
        top_three = process_exercise(
            video_path=video_path,
            exercise_rules=exercise_rules,
            vectorizer=vectorizer,
            exercise_names=exercise_names,
            detect_script_path=detect_script_path,
            yolov7_weights_path=yolov7_weights_path,
            conf_threshold=0.25,
            img_size=640
        )
        is_correct = actual_exercise in [ex for ex, _ in top_three]
        results.append({
            "Video Path": video_path,
            "Actual Exercise": actual_exercise,
            "Top 1": top_three[0][0],
            "Top 1 Confidence (%)": f"{top_three[0][1]:.2f}",
            "Top 2": top_three[1][0],
            "Top 2 Confidence (%)": f"{top_three[1][1]:.2f}",
            "Top 3": top_three[2][0],
            "Top 3 Confidence (%)": f"{top_three[2][1]:.2f}",
            "Actual Exercise in Top 3": "Yes" if is_correct else "No"
        })
    
    df = pd.DataFrame(results)
    output_path = "exercise_recognition_results.xlsx"
    df.to_excel(output_path, index=False)
    print(f"Recognition results saved to {output_path}")

if __name__ == "__main__":
    main()
