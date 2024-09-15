# Generate leg rule
from joint_keys import STRAIGHT, CLOSE, SPREAD
from math_helper import calculate_angle, calculate_distance
def generate_leg_rules(joint_positions):
    # Example rule for leg extension
    # left side and right side should have same logic with a different keyword
    rules  = {}
    rules.update(generator(joint_positions, 'left'))
    rules.update(generator(joint_positions, 'right'))
    return rules

def generator(joint_positions, keyword):
    rules = {}
    if SPREAD<abs(joint_positions['left_knee'][0] - joint_positions['right_knee'][0]) :
        rules['leg_position'] = 'Spread'
    if (STRAIGHT>abs(180-calculate_angle(joint_positions[f'{keyword}_hip'],joint_positions[f'{keyword}_knee'],joint_positions[f'{keyword}_foot']))):
        rules[f'{keyword}_leg_extension'] = 'extended'
    
    return rules