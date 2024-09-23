# rules_generation.py
from postures import determine_posture
from exercise import generate_exercise_rules
from arms import generate_arm_rules
from legs import generate_leg_rules

def generate_joint_rules(joint_positions:dict)->dict:
    rules = {}

    # Get rules from each module
    posture_rules = determine_posture(joint_positions)
    arm_rules = generate_arm_rules(joint_positions)
    leg_rules = generate_leg_rules(joint_positions)
    #exercise_rules = generate_exercise_rules(joint_positions)

    # List of all rule dictionaries
    all_rules = [posture_rules, arm_rules, leg_rules]

    # Merge the dictionaries
    for rule_dict in all_rules:
        for key, value in rule_dict.items():
            if key in rules:
                if isinstance(value, list):
                    rules[key].extend(value)
                else:
                    rules[key].append(value)
            else:
                rules[key] = value if isinstance(value, list) else [value]

    return rules
