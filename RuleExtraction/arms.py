# rule generation for arms
from joint_keys import STRAIGHT, CLOSE, SPREAD
from math_helper import calculate_angle, calculate_distance

def generate_arm_rules(joint_positions):

    # Example rule for arm position
    # left side and right side should have same logic with a different keyword
    rules  = {}
    rules.update(generator(joint_positions, 'left'))
    rules.update(generator(joint_positions, 'right'))
    return rules

def generator(joint_positions,keyword):
    rules = {}
    if SPREAD<abs(joint_positions['left_wrist'][0] - joint_positions['right_wrist'][0]) :
        rules['arm_position'] = 'Spread'
    return rules