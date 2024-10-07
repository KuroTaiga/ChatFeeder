# arms.py

from constants import STRAIGHT, CLOSE, SPREAD, ARM_KEYS
from helper import calculate_angle, calculate_distance, get_empty_arm_position,get_empty_arm_motion,get_arm_landmarks
def determine_arm_position_rule(joint_positions: dict) -> dict:
    """
    Generate position rules for arms based on joint positions.
    :param joint_positions: The dictionary of joint positions from pose detection.
    :return: A dictionary of arm landmarks with positions.
    """
    arm_landmarks = get_empty_arm_position()

    # Example logic: determine the position of the elbows and wrists based on joint positions
    if joint_positions['left_elbow']:
        arm_landmarks["left_elbow"]["position"].append("flexed")  # Example condition
    if joint_positions['right_elbow']:
        arm_landmarks["right_elbow"]["position"].append("extended")  # Example condition

    # Repeat similar logic for wrists or other conditions

    return arm_landmarks


def determine_arm_motion_rule(joint_positions_over_time: list) -> dict:
    """
    Generate motion rules for arms based on joint positions over time.
    :param joint_positions_over_time: A list of joint positions across multiple frames.
    :return: A dictionary of arm landmarks with motions.
    """
    arm_landmarks = get_empty_arm_motion()

    # Example logic: analyze motion based on joint positions over time
    for frame in joint_positions_over_time:
        # Check movement between frames for arms
        if frame['left_elbow']:
            arm_landmarks["left_elbow"]["motion"].append("extension")  # Example condition

    return arm_landmarks

def old_generate_arm_rules(joint_positions:dict)->dict:
    """
    Generates rules related to arm positions based on joint positions.

    Args:
        joint_positions (dict): A dictionary containing the coordinates of various joints.

    Returns:
        dict: A dictionary containing detected arm-related rules.
    """
    # Initialize the rules dictionary with empty lists
    rules = {key: [] for key in ARM_KEYS}

    # Global check for arms spread
    if SPREAD < abs(joint_positions['left_wrist'][0] - joint_positions['right_wrist'][0]):
        rules['arm_position'].append('spread')

    # Generate rules for each side
    for side in ['left', 'right']:
        side_rules = generate_side_arm_rules(joint_positions, side)
        # Update the main rules dictionary
        for key in side_rules:
            if key in rules:
                rules[key].extend(side_rules[key])
            else:
                rules[key] = side_rules[key]

    return rules

def generate_side_arm_rules(joint_positions:dict, side:str)->dict:
    """
    Generates side-specific arm rules.

    Args:
        joint_positions (dict): A dictionary containing the coordinates of various joints.
        side (str): 'left' or 'right' indicating which side to analyze.

    Returns:
        dict: A dictionary containing side-specific arm rules.
    """
    rules = {f'{side}_arm_position': []}

    elbow_x = joint_positions[f'{side}_elbow'][0]
    shoulder_x = joint_positions[f'{side}_shoulder'][0]
    wrist_y = joint_positions[f'{side}_wrist'][1]
    shoulder_y = joint_positions[f'{side}_shoulder'][1]
    elbow_y = joint_positions[f'{side}_elbow'][1]

    # Check if the elbow is driving back
    if side == 'left':
        if elbow_x < shoulder_x:
            rules[f'{side}_arm_position'].append('elbow_back')
    else:  # side == 'right'
        if elbow_x > shoulder_x:
            rules[f'{side}_arm_position'].append('elbow_back')

    # Check if the arm is raised
    if wrist_y < shoulder_y:
        rules[f'{side}_arm_position'].append('arm_raised')

    # Check if the arm is bent
    arm_angle = calculate_angle(
        joint_positions[f'{side}_shoulder'],
        joint_positions[f'{side}_elbow'],
        joint_positions[f'{side}_wrist']
    )
    if abs(arm_angle - 180) > STRAIGHT:
        rules[f'{side}_arm_position'].append('arm_bent')
    else:
        rules[f'{side}_arm_position'].append('arm_straight')

    # Add more side-specific checks as needed

    return rules
