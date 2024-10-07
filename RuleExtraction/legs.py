# legs.py
# leg rules generation using anatomical terms
# it includes movement and position of left and right sides of food/ankle, knees and hip

#feet: dorsiflexion and plantar flextion, inversion and eversion
#knee: lateral rotaion and medialk rotation
from constants import STRAIGHT, CLOSE, SPREAD, LEG_KEYS, SHOULDER_RANGE, FLEXED, BENT_RANGE
from helper import calculate_angle, calculate_distance, get_empty_leg_position, get_empty_leg_motion

def determine_leg_position_rule(joint_positions: dict) -> dict:
    """
    Generate position rules for legs (foot and knee) based on joint positions.
    :param joint_positions: The dictionary of joint positions from pose detection.
    :return: A dictionary of leg landmarks with positions.
    """
    leg_rules = {
        "left_knee": {"position": []},
        "right_knee": {"position": []},
        "left_foot": {"position": []},
        "right_foot": {"position": []}
    }

    left_foot = joint_positions.get('left_foot', {'x': None, 'y': None})
    right_foot = joint_positions.get('right_foot', {'x': None, 'y': None})
    left_knee = joint_positions.get('left_knee', {'x': None, 'y': None})
    right_knee = joint_positions.get('right_knee', {'x': None, 'y': None})
    left_hip = joint_positions.get('left_hip', {'x': None, 'y': None})
    right_hip = joint_positions.get('right_hip', {'x': None, 'y': None})

    # Foot position rules
    if left_foot['y'] and right_foot['y']:
        # Check if feet are on the ground
        leg_rules["left_foot"]["position"].append("on ground")
        leg_rules["right_foot"]["position"].append("on ground")
        
        # Check if feet are flat (y-coordinates similar)
        if abs(left_foot['y'] - right_foot['y']) < 0.02:
            leg_rules["left_foot"]["position"].append("flat")
            leg_rules["right_foot"]["position"].append("flat")
        
        # Shoulder-width apart check (distance between feet relative to shoulder width)
        left_shoulder = joint_positions.get('left_shoulder', {'x': None, 'y': None})
        right_shoulder = joint_positions.get('right_shoulder', {'x': None, 'y': None})
        
        if all([left_shoulder['x'], right_shoulder['x'], left_foot['x'], right_foot['x']]):
            shoulder_distance = abs(left_shoulder['x'] - right_shoulder['x'])
            foot_distance = abs(left_foot['x'] - right_foot['x'])
            
            if 0.9 * shoulder_distance <= foot_distance <= SHOULDER_RANGE * shoulder_distance:  # Within ~10% of shoulder width
                leg_rules["left_foot"]["position"].append("shoulder-width apart")
                leg_rules["right_foot"]["position"].append("shoulder-width apart")

    # Placeholder for "on bench" rule
    if False:  # Placeholder logic, to be updated
        leg_rules["left_foot"]["position"].append("on bench")
        leg_rules["right_foot"]["position"].append("on bench")

    # Knee position rules
    if all([left_hip['x'], left_knee['x'], left_foot['x']]):
        # Calculate the angle for the left knee
        left_knee_angle = calculate_angle(left_hip, left_knee, left_foot)
        if left_knee_angle is not None:
            if left_knee_angle < FLEXED:
                leg_rules["left_knee"]["position"].append("flexed")
            elif BENT_RANGE> abs(left_knee_angle-FLEXED):
                leg_rules["left_knee"]["position"].append("bent at 90 degrees")
            else:
                leg_rules["left_knee"]["position"].append("bent")

    if all([right_hip['x'], right_knee['x'], right_foot['x']]):
        # Calculate the angle for the right knee
        right_knee_angle = calculate_angle(right_hip, right_knee, right_foot)
        if right_knee_angle is not None:
            if right_knee_angle < FLEXED:
                leg_rules["right_knee"]["position"].append("flexed")
            elif BENT_RANGE> abs(right_knee_angle-FLEXED):
                leg_rules["right_knee"]["position"].append("bent at 90 degrees")
            else:
                leg_rules["right_knee"]["position"].append("bent")

    return leg_rules


def determine_leg_motion_rule(joint_positions_over_time: list) -> dict:
    """
    Generate motion rules for legs based on joint positions over time.
    :param joint_positions_over_time: A list of joint positions across multiple frames.
    :return: A dictionary of leg landmarks with motions.
    """
    leg_landmarks = get_empty_leg_motion()
    # Example logic: analyze motion based on joint positions over time
    for frame in joint_positions_over_time:
        # Check movement between frames for legs
        if frame['left_knee']:
            leg_landmarks["left_knee"]["motion"].append("flexion")  # Example condition

    return leg_landmarks

def old_generate_leg_rules(joint_positions:dict)->dict:
    """
    Generates rules related to leg positions based on joint positions.

    Args:
        joint_positions (dict): A dictionary containing the coordinates of various joints.

    Returns:
        dict: A dictionary containing detected leg-related rules.
    """
    # Initialize the rules dictionary with empty lists
    rules = {key: [] for key in LEG_KEYS}

    # Global checks for legs (if any)
    # Example: Check if legs are spread apart
    if SPREAD < abs(joint_positions['left_hip'][0] - joint_positions['right_hip'][0]):
        rules['leg_position'].append('spread')

    # Generate rules for each side
    for side in ['left', 'right']:
        side_rules = generate_side_leg_rules(joint_positions, side)
        # Update the main rules dictionary
        for key in side_rules:
            if key in rules:
                rules[key].extend(side_rules[key])
            else:
                rules[key] = side_rules[key]

    return rules

def generate_side_leg_rules(joint_positions:dict, side:str)->dict:
    """
    Generates side-specific leg rules.

    Args:
        joint_positions (dict): A dictionary containing the coordinates of various joints.
        side (str): 'left' or 'right'

    Returns:
        dict: A dictionary containing detected side-specific leg-related rules.
    """
    rules = {f'{side}_leg_position': []}

    # Retrieve joint positions
    hip = joint_positions.get(f'{side}_hip')
    knee = joint_positions.get(f'{side}_knee')
    ankle = joint_positions.get(f'{side}_ankle')

    # Ensure all required joints are present
    if hip and knee and ankle:
        # Calculate the angle at the knee joint
        leg_angle = calculate_angle(hip, knee, ankle)

        # Check if the leg is extended (straight)
        if abs(leg_angle - 180) < STRAIGHT:
            rules[f'{side}_leg_position'].append('extended')

        # Check if the leg is bent
        elif leg_angle < (180 - STRAIGHT):
            rules[f'{side}_leg_position'].append('bent')

        # Additional checks can be added here
        # For example, check if the leg is lifted
        if knee[1] < hip[1]:
            rules[f'{side}_leg_position'].append('lifted')
    else:
        # Handle cases where joints are missing
        rules[f'{side}_leg_position'].append('joint_data_missing')

    return rules
