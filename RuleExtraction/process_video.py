import cv2
from GYMDetector import YOLOv7EquipmentDetector, PoseDetector
from collections import Counter
from torso import determine_torsal_motion_rule, determine_torsal_position_rule
from arms import determine_arm_motion_rule,determine_arm_position_rule
from legs import determine_leg_motion_rule,determine_leg_position_rule
from helper import get_empty_landmarks,get_empty_motion,get_empty_position

def process_video(eqpt_detector: YOLOv7EquipmentDetector, pose_detector: PoseDetector, video_path: str) -> tuple:
    """
    Process an MP4 video and detect equipment, poses, and other mirrored attributes.
    :param eqpt_detector: Instance of YOLOv7EquipmentDetector for equipment detection.
    :param pose_detector: Instance of PoseDetector for pose detection.
    :param video_path: Path to the MP4 video file.
    :return: Tuple of (pose_dict, equipment_dict, other_dict)
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Error: Could not open video file {video_path}")
    
    frame_count = 0
    equipment_counter = Counter()
    pose_dict = get_empty_landmarks()
    other_dict = {}
    joint_pose_overtime = []

    while cap.isOpened():
        ret, frame = cap.read()  # Read each frame from the video
        if not ret:
            break  # If there are no more frames, break the loop

        # Detect equipment in the current frame
        detected_equipment = eqpt_detector.detect_equipment(frame)
        
        # Detect pose and generate joint rules
        joint_position_from_frame = pose_detector.get_joint_positions_from_frame(frame)
        joint_pose_overtime.append(joint_position_from_frame)
        frame_pose_rules = generate_position_rules(joint_position_from_frame)
        for landmark in pose_dict:
            pose_dict[landmark]["position"].extend(frame_pose_rules.get(landmark,{}).get("position",[]))
        # Update the equipment counter with detected equipment from this frame
        equipment_counter.update(detected_equipment)

        frame_count += 1
    video_motion_rules = generate_motion_rules(joint_pose_overtime)
    for landmark in pose_dict:
        pose_dict[landmark]["motion"].extend(video_motion_rules.get(landmark, {}).get("motion", []))
    # Release the video capture object
    cap.release()

    # Get the top 3 most detected equipment by count
    top_3_equipment = equipment_counter.most_common(3)

    # Format the top 3 equipment into the desired dictionary format
    equipment_dict = {
        "equipment": {
            "type": [item for item, _ in top_3_equipment],
            "bench incline": []
        }
    }

    # Check if "bench" is in the top detected equipment, and add incline if needed
    if "bench" in equipment_dict["equipment"]["type"]:
        # Placeholder for bench incline detection, needs further development.
        equipment_dict["equipment"]["bench incline"] = ["45"]  # Example incline

    # Populate other_dict with mirrored attribute
    other_dict = {
        "other": {
            "mirrored": "true"  # Placeholder for mirrored status, can be dynamically updated
        }
    }

    return pose_dict, equipment_dict, other_dict


def generate_position_rules(joint_positions: dict) -> dict:
    """
    Generate position rules based on joint positions from the current frame.
    :param joint_positions: The dictionary of joint positions from pose detection.
    :return: A dictionary of body landmarks with positions for each body part.
    """
    # Initialize the body landmarks dictionary with empty lists for positions
    body_landmarks = get_empty_position()

    # Get position rules from each module
    torso_position = determine_torsal_position_rule(joint_positions)
    arm_position = determine_arm_position_rule(joint_positions)
    leg_position = determine_leg_position_rule(joint_positions)

    # List of all position rule dictionaries
    all_position_rules = [torso_position, arm_position, leg_position]

    # Merge the position rules
    for rule_dict in all_position_rules:
        for landmark, values in rule_dict.items():
            if landmark in body_landmarks:
                body_landmarks[landmark]["position"].extend(values.get("position", []))

    # Remove duplicates from the 'position' lists
    for landmark in body_landmarks:
        body_landmarks[landmark]["position"] = list(set(body_landmarks[landmark]["position"]))

    return body_landmarks


def generate_motion_rules(joint_positions_over_time: list) -> dict:
    """
    Generate motion rules based on joint positions from multiple frames.
    :param joint_positions_over_time: A list of joint positions across multiple frames.
    :return: A dictionary of body landmarks with motions for each body part.
    """
    # Initialize the body landmarks dictionary with empty lists for motions
    body_landmarks = get_empty_motion()

    # Get motion rules from each module
    torso_motion = determine_torsal_motion_rule(joint_positions_over_time)
    arm_motion = determine_arm_motion_rule(joint_positions_over_time)
    leg_motion = determine_leg_motion_rule(joint_positions_over_time)

    # List of all motion rule dictionaries
    all_motion_rules = [torso_motion, arm_motion, leg_motion]

    # Merge the motion rules
    for rule_dict in all_motion_rules:
        for landmark, values in rule_dict.items():
            if landmark in body_landmarks:
                body_landmarks[landmark]["motion"].extend(values.get("motion", []))

    # Remove duplicates from the 'motion' lists
    for landmark in body_landmarks:
        body_landmarks[landmark]["motion"] = list(set(body_landmarks[landmark]["motion"]))

    return body_landmarks

