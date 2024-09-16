# Rules genereation for specific excercises
from constants import EXERCISE_KEYS, LYING_FLAT_THRESHOLD, ARM_RAISED_THRESHOLD

def generate_exercise_rules(joint_positions:dict)->dict:
    """
    Generates rules specific to certain exercises based on joint positions.

    Args:
        joint_positions (dict): A dictionary containing the coordinates of various joints.

    Returns:
        dict: A dictionary containing lists of strings representing detected exercise-specific rules.
    """
    # Initialize the rules dictionary with empty lists
    exercise_rules = {key: [] for key in EXERCISE_KEYS}
    return exercise_rules
    # Specific exercise rules for 30 different movements
    #

    
    # Abdominals Stretch
    # if abs(joint_positions['left_hip'][1] - joint_positions['left_ankle'][1]) < 50 and abs(joint_positions['left_shoulder'][1] - joint_positions['back'][1]) < 20:
    #     rules['posture'] = 'lying_flat'
    # if joint_positions['left_wrist'][1] < joint_positions['left_shoulder'][1] and joint_positions['right_wrist'][1] < joint_positions['right_shoulder'][1]:
    #     rules['arm_position'] = 'arms_overhead'

    # # Alternating Overhead Press
    # if joint_positions['left_wrist'][1] < joint_positions['left_shoulder'][1] or joint_positions['right_wrist'][1] < joint_positions['right_shoulder'][1]:
    #     rules['arm_position'] = 'one_arm_raised'

    # # Arnold Press
    # if joint_positions['left_wrist'][1] < joint_positions['left_shoulder'][1] and joint_positions['right_wrist'][1] < joint_positions['right_shoulder'][1]:
    #     rules['arm_position'] = 'both_arms_raised'

    # # Assisted Bulgarian Split Squat
    # if abs(joint_positions['left_knee'][0] - joint_positions['right_knee'][0]) > 50 and joint_positions['left_knee'][1] > joint_positions['left_hip'][1]:
    #     rules['legs'] = 'staggered_with_knee_bent'

    # # Ball Hamstring Curl
    # if abs(joint_positions['left_hip'][1] - joint_positions['left_shoulder'][1]) < 50 and joint_positions['left_foot'][1] > joint_positions['left_knee'][1]:
    #     rules['posture'] = 'lying_with_knees_bent'

    # # Band Bayesian Hammer Curl
    # if joint_positions['left_wrist'][1] > joint_positions['left_elbow'][1] and joint_positions['right_wrist'][1] > joint_positions['right_elbow'][1]:
    #     rules['arm_position'] = 'arms_bent'

    # # Band Front Raise
    # if joint_positions['left_wrist'][1] < joint_positions['left_shoulder'][1] and joint_positions['right_wrist'][1] < joint_positions['right_shoulder'][1]:
    #     rules['arm_position'] = 'arms_raised_to_shoulder'

    # # Band Glute Kickback
    # if abs(joint_positions['left_knee'][1] - joint_positions['right_knee'][1]) > 50 and joint_positions['left_foot'][1] < joint_positions['left_knee'][1]:
    #     rules['leg_position'] = 'leg_extended_back'

    # # Band Hammer Curl
    # if joint_positions['left_wrist'][1] > joint_positions['left_elbow'][1] and joint_positions['right_wrist'][1] > joint_positions['right_elbow'][1]:
    #     rules['arm_position'] = 'arms_bent'

    # # Band High Hammer Curl
    # if joint_positions['left_wrist'][1] < joint_positions['left_shoulder'][1] and joint_positions['right_wrist'][1] < joint_positions['right_shoulder'][1]:
    #     rules['arm_position'] = 'high_arms_bent'

    # # Band Lateral Raise
    # if joint_positions['left_wrist'][1] < joint_positions['left_shoulder'][1] and joint_positions['right_wrist'][1] < joint_positions['right_shoulder'][1]:
    #     rules['arm_position'] = 'arms_extended_to_sides'

    # # Band Skullcrusher
    # if joint_positions['left_wrist'][1] > joint_positions['left_shoulder'][1] and joint_positions['right_wrist'][1] > joint_positions['right_shoulder'][1]:
    #     rules['arm_position'] = 'arms_behind_head'

    # # Band Squat
    # if joint_positions['left_knee'][1] > joint_positions['left_hip'][1] and joint_positions['right_knee'][1] > joint_positions['right_hip'][1]:
    #     rules['legs'] = 'squat_position'

    # # Band Wood Chopper
    # if abs(joint_positions['left_wrist'][1] - joint_positions['right_wrist'][1]) > 50:
    #     rules['arm_position'] = 'diagonal_pull'

    # # Barbell Curtsy Lunge
    # if joint_positions['left_knee'][1] > joint_positions['left_hip'][1] and abs(joint_positions['left_knee'][0] - joint_positions['right_knee'][0]) > 50:
    #     rules['posture'] = 'curtsy_lunge_with_barbell'

    # # Barbell Bench Press
    # if abs(joint_positions['left_shoulder'][1] - joint_positions['back'][1]) < 20 and joint_positions['left_wrist'][1] < joint_positions['left_shoulder'][1]:
    #     rules['posture'] = 'lying_with_arms_raised'

    # # Barbell Bulgarian Split Squat
    # if abs(joint_positions['left_knee'][0] - joint_positions['right_knee'][0]) > 50 and joint_positions['left_knee'][1] > joint_positions['left_hip'][1]:
    #     rules['legs'] = 'staggered_with_knee_bent'

    # # Barbell Close Grip Bench Press
    # if joint_positions['left_wrist'][0] - joint_positions['right_wrist'][0] < 20 and joint_positions['left_wrist'][1] < joint_positions['left_shoulder'][1]:
    #     rules['posture'] = 'lying_with_close_grip'

    # # Barbell Front Raise
    # if joint_positions['left_wrist'][1] < joint_positions['left_shoulder'][1] and joint_positions['right_wrist'][1] < joint_positions['right_shoulder'][1]:
    #     rules['arm_position'] = 'barbell_front_raise'

    # # Barbell High Bar Squat
    # if joint_positions['left_knee'][1] > joint_positions['left_hip'][1] and joint_positions['left_hip'][1] < joint_positions['left_shoulder'][1]:
    #     rules['posture'] = 'squat_with_barbell_high_bar'

    # # Barbell Low Bar Squat
    # if joint_positions['left_knee'][1] > joint_positions['left_hip'][1] and joint_positions['left_hip'][1] < joint_positions['left_shoulder'][1]:
    #     rules['posture'] = 'squat_with_barbell_low_bar'

    # # Barbell Seated Calf Raise
    # if joint_positions['left_knee'][1] > joint_positions['left_hip'][1] and joint_positions['left_foot'][1] > joint_positions['left_knee'][1]:
    #     rules['posture'] = 'seated_calf_raise'

    # # Kettlebell Hip Thrust
    # if joint_positions['left_hip'][1] < joint_positions['left_shoulder'][1] and joint_positions['left_foot'][1] > joint_positions['left_knee'][1]:
    #     rules['posture'] = 'hip_thrust_with_kettlebell'

    # # Neutral Seated Overhead Press
    # if joint_positions['left_wrist'][1] < joint_positions['left_shoulder'][1] and joint_positions['right_wrist'][1] < joint_positions['right_shoulder'][1]:
    #     rules['arm_position'] = 'seated_overhead_press'

    # # Staggered Hip Thrust
    # if joint_positions['left_foot'][1] < joint_positions['right_foot'][1] and joint_positions['left_hip'][1] < joint_positions['left_shoulder'][1]:
    #     rules['posture'] = 'staggered_hip_thrust'

    # # Supermans
    # if abs(joint_positions['nose'][1] - joint_positions['back'][1]) < 20 and joint_positions['left_wrist'][1] < joint_positions['left_shoulder'][1] and joint_positions['left_foot'][1] < joint_positions['left_knee'][1]:
    #     rules['posture'] = 'supermans_pose'

    # # Windmill
    # if joint_positions['right_hand'][1] < joint_positions['right_shoulder'][1] and abs(joint_positions['left_foot'][0] - joint_positions['right_foot'][0]) > 50:
    #     rules['exercise'] = 'windmill_pose'
