# postures.py
from constants import LEAN, NEUTRAL_SPINE,UPRIGHT, STANDING, BENT, HIP_HINGE_ANGLE_THRESHOLD,CORE_ENGAGEMENT_THRESHOLD
from helper import calculate_distance, calculate_angle, get_empty_torso_position, get_empty_torso_motion
def determine_torsal_rule(joint_positions: dict, joint_positions_over_time: list) -> dict:
    """
    Combine position and motion rules for the torso, left hip, right hip, and shoulders.
    :param joint_positions: Joint positions for the current frame (for position rules).
    :param joint_positions_over_time: List of joint positions across all frames (for motion rules).
    :return: Dictionary with position and motion rules for torso, hips, and shoulders.
    """
    # Get the position rules for the current frame
    position_rules = determine_torsal_position_rule(joint_positions)
    
    # Get the motion rules based on all frames
    motion_rules = determine_torsal_motion_rule(joint_positions_over_time)

    # Combine position and motion rules into the final format
    torsal_rules = {
        "torso": {"position": position_rules.get("torso", {}).get("position", []), 
                  "motion": motion_rules.get("torso", {}).get("motion", [])},
        "left_hip": {"position": position_rules.get("left_hip", {}).get("position", []), 
                     "motion": motion_rules.get("left_hip", {}).get("motion", [])},
        "right_hip": {"position": position_rules.get("right_hip", {}).get("position", []), 
                      "motion": motion_rules.get("right_hip", {}).get("motion", [])},
        "left_shoulder": {"position": position_rules.get("left_shoulder", {}).get("position", []), 
                          "motion": motion_rules.get("left_shoulder", {}).get("motion", [])},
        "right_shoulder": {"position": position_rules.get("right_shoulder", {}).get("position", []), 
                           "motion": motion_rules.get("right_shoulder", {}).get("motion", [])}
    }

    return torsal_rules

def determine_torsal_position_rule(joint_positions: dict) -> dict:
    """
    Determine the position of the torso, left hip, right hip, and shoulders for a single frame.
    :param joint_positions: Dictionary containing the joint positions from pose detection.
    :return: Dictionary with position rules for torso, hips, and shoulders.
    """
    position_rules = get_empty_torso_position()
    left_shoulder = joint_positions.get('left_shoulder', {'x': None, 'y': None})
    right_shoulder = joint_positions.get('right_shoulder', {'x': None, 'y': None})
    left_hip = joint_positions.get('left_hip', {'x': None, 'y': None})
    right_hip = joint_positions.get('right_hip', {'x': None, 'y': None})

    if all([left_shoulder['y'], right_shoulder['y'], left_hip['y'], right_hip['y']]):
        # Calculate vertical distance between shoulders and hips
        shoulder_avg_y = (left_shoulder['y'] + right_shoulder['y']) / 2
        hip_avg_y = (left_hip['y'] + right_hip['y']) / 2

        # Calculate torso leaning direction
        shoulder_avg_x = (left_shoulder['x'] + right_shoulder['x']) / 2
        hip_avg_x = (left_hip['x'] + right_hip['x']) / 2

        vertical_distance = abs(shoulder_avg_y - hip_avg_y)
        horizontal_distance = abs(shoulder_avg_x - hip_avg_x)

        # Torso position rules
        if vertical_distance > UPRIGHT:  # Example threshold for upright
            position_rules["torso"]["position"].append("upright")

        if horizontal_distance < NEUTRAL_SPINE:  # Neutral spine if hips and shoulders align
            position_rules["torso"]["position"].append("neutral spine")

        if shoulder_avg_x > hip_avg_x + LEAN:  # Leaning forward (shoulders in front of hips)
            position_rules["torso"]["position"].append("leaning forward")

        if shoulder_avg_x < hip_avg_x - LEAN:  # Leaning backward (shoulders behind hips)
            position_rules["torso"]["position"].append("leaning backward")

        # Placeholder for "on bench"
        if False:  # Currently a placeholder, logic needs to be implemented
            position_rules["torso"]["position"].append("on bench")
    else:
        raise ValueError("Need to handle missing joints")
    return position_rules


def determine_torsal_motion_rule(joint_positions_over_time: list) -> dict:
    """
    Determine the motion of the torso, left hip, right hip, and shoulders over multiple frames.
    :param joint_positions_over_time: List of joint positions across all frames.
    :return: Dictionary with motion rules for torso, hips, and shoulders.
    """
    motion_rules = get_empty_torso_motion()

    def is_stationary(motion_history):
        """Helper function to check if a body part has remained stationary."""
        return all(x == motion_history[0] for x in motion_history)

    # Analyze motion over time for each body part
    for body_part in ["torso", "left_hip", "right_hip", "left_shoulder", "right_shoulder"]:
        positions = [(frame[body_part]["x"], frame[body_part]["y"]) for frame in joint_positions_over_time if body_part in frame]

        if len(positions) > 1:
            x_positions = [pos[0] for pos in positions]
            y_positions = [pos[1] for pos in positions]
            
            # Determine motion for each body part
            if is_stationary(x_positions) and is_stationary(y_positions):
                motion_rules[body_part]["motion"].append("stationary")
            else:
                motion_rules[body_part]["motion"].append("moving")

    return motion_rules
