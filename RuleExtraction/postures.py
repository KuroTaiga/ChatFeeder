# postures.py

def determine_posture(joint_positions):
    posture = 'unknown'
    if abs(joint_positions['left_shoulder'][1] - joint_positions['left_hip'][1]) < 20:
        posture = 'standing'
    elif abs(joint_positions['left_shoulder'][1] - joint_positions['back'][1]) < 15:
        posture = 'upright'
    elif abs(joint_positions['left_shoulder'][1] - joint_positions['left_hip'][1]) > 40:
        posture = 'bent'
    else:
        posture = 'hip_hinge'
    # sitterd?
    
    return posture
