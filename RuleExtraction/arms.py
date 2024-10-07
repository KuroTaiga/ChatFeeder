# arms.py

from constants import STRAIGHT, CLOSE, SPREAD, ARM_KEYS, OUTWARD, INWARD, FLEXED, BENT_RANGE
from helper import calculate_angle, calculate_distance, get_empty_arm_position,get_empty_arm_motion,get_arm_landmarks
def determine_arm_position_rule(joint_positions: dict) -> dict:
    """
    Generate position rules for arms (hand and elbow) based on joint positions.
    :param joint_positions: The dictionary of joint positions from pose detection.
    :return: A dictionary of arm landmarks with positions.
    """
    arm_rules = {
        "left_elbow": {"position": []},
        "right_elbow": {"position": []},
        "left_hand": {"position": []},
        "right_hand": {"position": []}
    }

    left_hand = joint_positions.get('left_hand', {'x': None, 'y': None})
    right_hand = joint_positions.get('right_hand', {'x': None, 'y': None})
    left_elbow = joint_positions.get('left_elbow', {'x': None, 'y': None})
    right_elbow = joint_positions.get('right_elbow', {'x': None, 'y': None})
    left_shoulder = joint_positions.get('left_shoulder', {'x': None, 'y': None})
    right_shoulder = joint_positions.get('right_shoulder', {'x': None, 'y': None})
    torso = joint_positions.get('torso', {'x': None, 'y': None})  # Use for relative position checks

    # Hand position rules
    if left_hand['x'] and left_hand['y']:
        if left_hand['y'] < left_shoulder['y']:
            arm_rules["left_hand"]["position"].append("vertical upward")
        else:
            arm_rules["left_hand"]["position"].append("vertical downward")
        
        # Check if left hand is horizontally outward from the torso
        if abs(left_hand['x'] - left_shoulder['x']) > OUTWARD:  # Example threshold
            arm_rules["left_hand"]["position"].append("horizontal outward")
        elif abs(left_hand['x'] - left_shoulder['x']) < INWARD:
            arm_rules["left_hand"]["position"].append("horizontal inward")

        # Placeholder logic for holding equipment
        arm_rules["left_hand"]["position"].append("holding equipment")  # Placeholder

        # Check if hand is over chest or head
        if torso and torso['y'] and left_hand['y'] < torso['y'] - CLOSE:
            arm_rules["left_hand"]["position"].append("over head")
        elif left_hand['y'] < torso['y'] + CLOSE:
            arm_rules["left_hand"]["position"].append("over chest")

    if right_hand['x'] and right_hand['y']:
        if right_hand['y'] < right_shoulder['y']:
            arm_rules["right_hand"]["position"].append("vertical upward")
        else:
            arm_rules["right_hand"]["position"].append("vertical downward")
        
        # Check if right hand is horizontally outward from the torso
        if abs(right_hand['x'] - right_shoulder['x']) > OUTWARD:  # Example threshold
            arm_rules["right_hand"]["position"].append("horizontal outward")
        elif abs(right_hand['x'] - right_shoulder['x']) < INWARD:
            arm_rules["right_hand"]["position"].append("horizontal inward")

        # Placeholder logic for holding equipment
        arm_rules["right_hand"]["position"].append("holding equipment")  # Placeholder

        # Check if hand is over chest or head
        if torso and torso['y'] and right_hand['y'] < torso['y'] - CLOSE:
            arm_rules["right_hand"]["position"].append("over head")
        elif right_hand['y'] < torso['y'] + CLOSE:
            arm_rules["right_hand"]["position"].append("over chest")

    # Elbow position rules
    if all([left_shoulder['x'], left_elbow['x'], left_hand['x']]):
        left_elbow_angle = calculate_angle(left_shoulder, left_elbow, left_hand)
        if left_elbow_angle:
            if left_elbow_angle < FLEXED:
                arm_rules["left_elbow"]["position"].append("flexed")
            elif  BENT_RANGE> abs(left_elbow_angle-FLEXED):
                arm_rules["left_elbow"]["position"].append("bent at 90 degrees")
            else:
                arm_rules["left_elbow"]["position"].append("extended")
        
        # Check if elbow is close to torso
        if abs(left_elbow['x'] - torso['x']) < CLOSE:  # Example threshold for closeness
            arm_rules["left_elbow"]["position"].append("close to torso")

    if all([right_shoulder['x'], right_elbow['x'], right_hand['x']]):
        right_elbow_angle = calculate_angle(right_shoulder, right_elbow, right_hand)
        if right_elbow_angle:
            if right_elbow_angle < FLEXED:
                arm_rules["right_elbow"]["position"].append("flexed")
            elif BENT_RANGE> abs(right_elbow_angle-FLEXED):
                arm_rules["right_elbow"]["position"].append("bent at 90 degrees")
            else:
                arm_rules["right_elbow"]["position"].append("extended")
        
        # Check if elbow is close to torso
        if abs(right_elbow['x'] - torso['x']) < CLOSE:  # Example threshold for closeness
            arm_rules["right_elbow"]["position"].append("close to torso")

    return arm_rules


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
