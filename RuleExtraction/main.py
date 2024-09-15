# main.py

from joint_keys import JOINT_KEYS
from rules_generation import generate_joint_rules
from exercise_parser import parse_exercise_description

# Simulate getting joint positions from a video feed
def get_joint_positions_from_video():
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

def process_exercise(description):
    joint_positions = get_joint_positions_from_video()  # Simulate joint position extraction
    actual_rules = generate_joint_rules(joint_positions)  # Generate rules based on actual positions
    expected_rules = parse_exercise_description(description)  # Parse expected rules from description
    matched = compare_joint_positions(actual_rules, expected_rules)

    if matched:
        print("Exercise performed correctly.")
    else:
        print("Exercise performance did not match the description.")

# Example usage for the specific kettlebell exercise
description = (
    "The person stands with feet shoulder-width apart, holding the kettlebell with both hands between the legs, "
    "while the torso leans slightly forward, engaging a hinge at the hips. With a controlled movement, "
    "the body maintains this forward, hinged posture as the hands bring the kettlebell upward toward the lower abdomen, "
    "driving the elbows back and engaging the back muscles, before reversing the motion smoothly, "
    "lowering the kettlebell back down in a steady, fluid arc without releasing the hip hinge."
)
for desc in description:
    print(f"\nProcessing: {desc}")
    process_exercise(desc)
