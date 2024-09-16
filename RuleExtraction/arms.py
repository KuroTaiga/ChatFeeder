# arms.py

from constants import STRAIGHT, CLOSE, SPREAD, ARM_KEYS
from math_helper import calculate_angle, calculate_distance

def generate_arm_rules(joint_positions:dict)->dict:
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
