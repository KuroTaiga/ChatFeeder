import math

# Helper function to calculate the angle between three points (for joint angle calculation)
def calculate_angle(a, b, c):
    ang = math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))
    return ang + 360 if ang < 0 else ang

# Placeholder function to simulate extracting joint positions from video stream
def get_joint_positions_from_video():
    # Simulated joint positions focusing on relevant points (shoulders, elbows, wrists, hips, knees, and ankles)
    joint_positions = {
        'left_shoulder': (80, 200),
        'right_shoulder': (120, 200),
        'left_elbow': (70, 250),
        'right_elbow': (130, 250),
        'left_wrist': (60, 300),
        'right_wrist': (140, 300),
        'left_hip': (90, 270),
        'right_hip': (110, 270),
        'left_knee': (85, 350),
        'right_knee': (115, 350),
        'left_ankle': (80, 400),
        'right_ankle': (120, 400)
    }
    return joint_positions


# Function to generate rules based on 30 joint positions (Joint Rule Extraction)
def generate_joint_rules(joint_positions):
    rules = {}

    # Posture based on shoulder and hip positions
    if abs(joint_positions['left_shoulder'][1] - joint_positions['left_hip'][1]) < 20:
        rules['posture'] = 'standing'
    elif abs(joint_positions['left_shoulder'][1] - joint_positions['back'][1]) < 15:
        rules['posture'] = 'upright'
    else:
        rules['posture'] = 'bent'

    # Leg positioning for squats, lunges, split squats, etc.
    if joint_positions['left_knee'][1] < joint_positions['left_hip'][1]:
        rules['legs'] = 'bent'
    elif abs(joint_positions['left_knee'][0] - joint_positions['right_knee'][0]) > 50:
        rules['legs'] = 'staggered'

    # Leg extension for hamstring curls or kickbacks
    # TODO: this extention for curl might be too simple? this only check for foot lower than knees
    # also need for both sides
    # OLD:
    # if joint_positions['left_foot'][1] > joint_positions['left_knee'][1]:
    #     rules['leg_extension'] = 'extended'
    # entened leg should be close to straight, hip, knee, foot angle should be close to 180
    if (10>abs(180-calculate_angle(joint_positions['left_hip'],joint_positions['left_knee'],joint_positions['left_foot']))):
        rules['left_leg_extension'] = 'extended'
    if (10>abs(180-calculate_angle(joint_positions['right_hip'],joint_positions['right_knee'],joint_positions['right_foot']))):
        rules['right_leg_extension'] = 'extended'
    # Arm positioning for curls, presses, or lateral raises
    # TODO: press doesn't follow this 'extended' rule
    if abs(joint_positions['left_wrist'][0] - joint_positions['right_wrist'][0]) > 50:
        rules['arm_position'] = 'extended'
    
    # Specific exercise rules for 30 different movements

    # Abdominals Stretch
    if abs(joint_positions['left_hip'][1] - joint_positions['left_ankle'][1]) < 50 and abs(joint_positions['left_shoulder'][1] - joint_positions['back'][1]) < 20:
        rules['posture'] = 'lying_flat'
    if joint_positions['left_wrist'][1] < joint_positions['left_shoulder'][1] and joint_positions['right_wrist'][1] < joint_positions['right_shoulder'][1]:
        rules['arm_position'] = 'arms_overhead'

    # Alternating Overhead Press
    if joint_positions['left_wrist'][1] < joint_positions['left_shoulder'][1] or joint_positions['right_wrist'][1] < joint_positions['right_shoulder'][1]:
        rules['arm_position'] = 'one_arm_raised'

    # Arnold Press
    if joint_positions['left_wrist'][1] < joint_positions['left_shoulder'][1] and joint_positions['right_wrist'][1] < joint_positions['right_shoulder'][1]:
        rules['arm_position'] = 'both_arms_raised'

    # Assisted Bulgarian Split Squat
    if abs(joint_positions['left_knee'][0] - joint_positions['right_knee'][0]) > 50 and joint_positions['left_knee'][1] > joint_positions['left_hip'][1]:
        rules['legs'] = 'staggered_with_knee_bent'

    # Ball Hamstring Curl
    if abs(joint_positions['left_hip'][1] - joint_positions['left_shoulder'][1]) < 50 and joint_positions['left_foot'][1] > joint_positions['left_knee'][1]:
        rules['posture'] = 'lying_with_knees_bent'

    # Band Bayesian Hammer Curl
    if joint_positions['left_wrist'][1] > joint_positions['left_elbow'][1] and joint_positions['right_wrist'][1] > joint_positions['right_elbow'][1]:
        rules['arm_position'] = 'arms_bent'

    # Band Front Raise
    if joint_positions['left_wrist'][1] < joint_positions['left_shoulder'][1] and joint_positions['right_wrist'][1] < joint_positions['right_shoulder'][1]:
        rules['arm_position'] = 'arms_raised_to_shoulder'

    # Band Glute Kickback
    if abs(joint_positions['left_knee'][1] - joint_positions['right_knee'][1]) > 50 and joint_positions['left_foot'][1] < joint_positions['left_knee'][1]:
        rules['leg_position'] = 'leg_extended_back'

    # Band Hammer Curl
    if joint_positions['left_wrist'][1] > joint_positions['left_elbow'][1] and joint_positions['right_wrist'][1] > joint_positions['right_elbow'][1]:
        rules['arm_position'] = 'arms_bent'

    # Band High Hammer Curl
    if joint_positions['left_wrist'][1] < joint_positions['left_shoulder'][1] and joint_positions['right_wrist'][1] < joint_positions['right_shoulder'][1]:
        rules['arm_position'] = 'high_arms_bent'

    # Band Lateral Raise
    if joint_positions['left_wrist'][1] < joint_positions['left_shoulder'][1] and joint_positions['right_wrist'][1] < joint_positions['right_shoulder'][1]:
        rules['arm_position'] = 'arms_extended_to_sides'

    # Band Skullcrusher
    if joint_positions['left_wrist'][1] > joint_positions['left_shoulder'][1] and joint_positions['right_wrist'][1] > joint_positions['right_shoulder'][1]:
        rules['arm_position'] = 'arms_behind_head'

    # Band Squat
    if joint_positions['left_knee'][1] > joint_positions['left_hip'][1] and joint_positions['right_knee'][1] > joint_positions['right_hip'][1]:
        rules['legs'] = 'squat_position'

    # Band Wood Chopper
    if abs(joint_positions['left_wrist'][1] - joint_positions['right_wrist'][1]) > 50:
        rules['arm_position'] = 'diagonal_pull'

    # Barbell Curtsy Lunge
    if joint_positions['left_knee'][1] > joint_positions['left_hip'][1] and abs(joint_positions['left_knee'][0] - joint_positions['right_knee'][0]) > 50:
        rules['posture'] = 'curtsy_lunge_with_barbell'

    # Barbell Bench Press
    if abs(joint_positions['left_shoulder'][1] - joint_positions['back'][1]) < 20 and joint_positions['left_wrist'][1] < joint_positions['left_shoulder'][1]:
        rules['posture'] = 'lying_with_arms_raised'

    # Barbell Bulgarian Split Squat
    if abs(joint_positions['left_knee'][0] - joint_positions['right_knee'][0]) > 50 and joint_positions['left_knee'][1] > joint_positions['left_hip'][1]:
        rules['legs'] = 'staggered_with_knee_bent'

    # Barbell Close Grip Bench Press
    if joint_positions['left_wrist'][0] - joint_positions['right_wrist'][0] < 20 and joint_positions['left_wrist'][1] < joint_positions['left_shoulder'][1]:
        rules['posture'] = 'lying_with_close_grip'

    # Barbell Front Raise
    if joint_positions['left_wrist'][1] < joint_positions['left_shoulder'][1] and joint_positions['right_wrist'][1] < joint_positions['right_shoulder'][1]:
        rules['arm_position'] = 'barbell_front_raise'

    # Barbell High Bar Squat
    if joint_positions['left_knee'][1] > joint_positions['left_hip'][1] and joint_positions['left_hip'][1] < joint_positions['left_shoulder'][1]:
        rules['posture'] = 'squat_with_barbell_high_bar'

    # Barbell Low Bar Squat
    if joint_positions['left_knee'][1] > joint_positions['left_hip'][1] and joint_positions['left_hip'][1] < joint_positions['left_shoulder'][1]:
        rules['posture'] = 'squat_with_barbell_low_bar'

    # Barbell Seated Calf Raise
    if joint_positions['left_knee'][1] > joint_positions['left_hip'][1] and joint_positions['left_foot'][1] > joint_positions['left_knee'][1]:
        rules['posture'] = 'seated_calf_raise'

    # Kettlebell Hip Thrust
    if joint_positions['left_hip'][1] < joint_positions['left_shoulder'][1] and joint_positions['left_foot'][1] > joint_positions['left_knee'][1]:
        rules['posture'] = 'hip_thrust_with_kettlebell'

    # Neutral Seated Overhead Press
    if joint_positions['left_wrist'][1] < joint_positions['left_shoulder'][1] and joint_positions['right_wrist'][1] < joint_positions['right_shoulder'][1]:
        rules['arm_position'] = 'seated_overhead_press'

    # Staggered Hip Thrust
    if joint_positions['left_foot'][1] < joint_positions['right_foot'][1] and joint_positions['left_hip'][1] < joint_positions['left_shoulder'][1]:
        rules['posture'] = 'staggered_hip_thrust'

    # Supermans
    if abs(joint_positions['nose'][1] - joint_positions['back'][1]) < 20 and joint_positions['left_wrist'][1] < joint_positions['left_shoulder'][1] and joint_positions['left_foot'][1] < joint_positions['left_knee'][1]:
        rules['posture'] = 'supermans_pose'

    # Windmill
    if joint_positions['right_hand'][1] < joint_positions['right_shoulder'][1] and abs(joint_positions['left_foot'][0] - joint_positions['right_foot'][0]) > 50:
        rules['exercise'] = 'windmill_pose'

    return rules

# Function to parse exercise description into rules
def parse_exercise_description(description):
    rules = {}
    
    # Parsing posture
    if 'standing' in description:
        rules['posture'] = 'standing'
    if 'lying flat' in description or 'lying face down' in description:
        rules['posture'] = 'lying'
    if 'upright' in description:
        rules['posture'] = 'upright'
    if 'seated' in description:
        rules['posture'] = 'seated'
    
    # Parsing leg positioning and actions
    if 'shoulder-width apart' in description:
        rules['legs'] = 'shoulder_width_apart'
    if 'squat' in description or 'lunge' in description or 'curtsy' in description:
        rules['legs'] = 'bent'
    if 'staggered' in description or 'split squat' in description:
        rules['legs'] = 'staggered'
    if 'leg extended' in description or 'kickback' in description:
        rules['leg_extension'] = 'extended'
    if 'calf raise' in description:
        rules['leg_extension'] = 'calf_raise'

    # Parsing arm positioning and actions
    if 'extend the arms' in description or 'arms extended' in description:
        rules['arm_position'] = 'extended'
    if 'bend in the elbow' in description or 'arms bent' in description:
        rules['arm_position'] = 'arms_bent'
    if 'arms raised overhead' in description or 'arms overhead' in description:
        rules['arm_position'] = 'arms_overhead'
    if 'front raise' in description:
        rules['arm_position'] = 'front_raise'
    if 'lateral raise' in description:
        rules['arm_position'] = 'lateral_raise'
    if 'hammer curl' in description:
        rules['arm_position'] = 'hammer_curl'
    if 'skullcrusher' in description:
        rules['arm_position'] = 'skullcrusher'
    if 'press' in description:
        rules['arm_position'] = 'press'
    if 'wood chopper' in description:
        rules['arm_position'] = 'wood_chopper'
    
    # Parsing complex actions like pushing, rotating, pulling
    if 'push' in description or 'press' in description:
        rules['action'] = 'push'
    if 'pull' in description:
        rules['action'] = 'pull'
    if 'rotate' in description or 'rotation' in description:
        rules['action'] = 'rotation'
    if 'twist' in description:
        rules['action'] = 'twist'
    
    # Parsing combination of movements
    if 'squat while pressing' in description or 'squat and press' in description:
        rules['combined_movement'] = 'squat_press'
    if 'lunge while raising' in description:
        rules['combined_movement'] = 'lunge_raise'
    if 'twist and press' in description or 'rotation and press' in description:
        rules['combined_movement'] = 'rotation_press'

    # Parsing leg extension
    if 'extend the leg' in description or 'leg extended' in description:
        rules['leg_extension'] = 'extended'

    return rules


# Function to compare actual joint positions with expected exercise description rules
def compare_joint_positions(actual_rules, expected_rules):
    matched = True
    for key in expected_rules:
        if key in actual_rules:
            if actual_rules[key] != expected_rules[key]:
                print(f"Mismatch on {key}: expected {expected_rules[key]}, but got {actual_rules[key]}")
                matched = False
        else:
            print(f"Missing rule for {key} in actual performance.")
            matched = False
    return matched

# Main function to simulate exercise processing
def process_exercise(description):
    joint_positions = get_joint_positions_from_video()
    actual_rules = generate_joint_rules(joint_positions)
    expected_rules = parse_exercise_description(description)
    matched = compare_joint_positions(actual_rules, expected_rules)

    if matched:
        print("Exercise performed correctly.")
    else:
        print("Exercise performance did not match the description.")

# Example usage with dynamic descriptions for different exercises
exercise_descriptions = [
    "......"
    # Add more descriptions as needed
]

# Process each exercise
for desc in exercise_descriptions:
    print(f"\nProcessing: {desc}")
    process_exercise(desc)
