# postures.py
from constants import STANDING, UPRIGHT, BENT, HIP_HINGE_ANGLE_THRESHOLD,CORE_ENGAGEMENT_THRESHOLD
from math_helper import calculate_distance, calculate_angle

def determine_posture(joint_positions:dict)->dict:
    postures = []  # Initialize an empty list to store detected postures

    left_vertical_distance = abs(joint_positions['left_shoulder'][1] - joint_positions['left_hip'][1])
    right_vertical_distance = abs(joint_positions['right_shoulder'][1] - joint_positions['right_hip'][1])

    # Check for bent posture first
    if left_vertical_distance > BENT and right_vertical_distance > BENT:
        postures.append('bent')
    # Check for standing posture
    elif left_vertical_distance < STANDING and right_vertical_distance < STANDING:
        postures.append('standing')
    # Check for upright posture
    elif left_vertical_distance < UPRIGHT and right_vertical_distance < UPRIGHT:
        postures.append('upright')
    else:
        # Check for hip hinge using angle
        angle = calculate_angle(
            joint_positions['left_knee'],
            joint_positions['left_hip'],
            joint_positions['left_shoulder']
        )
        if HIP_HINGE_ANGLE_THRESHOLD < angle < (180 - HIP_HINGE_ANGLE_THRESHOLD):
            postures.append('hip_hinge')
        else:
            postures.append('unknown_posture')

    # Check for core engagement (e.g., torso lean)
    shoulder_hip_distance = calculate_distance(joint_positions['left_shoulder'], joint_positions['left_hip'])
    if shoulder_hip_distance > CORE_ENGAGEMENT_THRESHOLD:
        postures.append('core_engaged')

    return {'posture': postures}  # Return the dictionary