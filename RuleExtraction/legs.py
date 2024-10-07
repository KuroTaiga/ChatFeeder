# legs.py
# leg rules generation using anatomical terms
# it includes movement and position of left and right sides of food/ankle, knees and hip

#feet: dorsiflexion and plantar flextion, inversion and eversion
#knee: lateral rotaion and medialk rotation
from constants import STRAIGHT, CLOSE, SPREAD, LEG_KEYS
from helper import calculate_angle, calculate_distance, get_empty_leg_position, get_empty_leg_motion
def determine_leg_position_rule(joint_positions: dict) -> dict:
    """
    Generate position rules for legs based on joint positions.
    :param joint_positions: The dictionary of joint positions from pose detection.
    :return: A dictionary of leg landmarks with positions.
    """
    leg_landmarks = get_empty_leg_position()

    # Example logic: determine the position of the knees and ankles
    if joint_positions['left_knee']:
        leg_landmarks["left_knee"]["position"].append("bent at 90 degrees")  # Example condition
    if joint_positions['right_knee']:
        leg_landmarks["right_knee"]["position"].append("flexed")  # Example condition

    return leg_landmarks


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
