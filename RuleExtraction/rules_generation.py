# rules_generation.py
from postures import determine_posture
from exercise import generate_exercise_rules
from arms import generate_arm_rules
from legs import generate_leg_rules

def generate_joint_rules(joint_positions):
    rules = {}
    rules.update(determine_posture(joint_positions))
    rules.update(generate_arm_rules(joint_positions))
    rules.update(generate_leg_rules(joint_positions))
    rules.update(generate_exercise_rules(joint_positions))
    return rules
