# constants.py

# Define the keys for the rules dictionary
RULE_KEYS = [
    'posture',
    'legs',
    'leg_extension',
    'arm_position',
    'left_arm_position',
    'right_arm_position',
    'action',
    'combined_movement'
]

# List of joint keys used in the system
JOINT_KEYS = [
    'left_shoulder', 'right_shoulder', 'left_elbow', 'right_elbow',
    'left_wrist', 'right_wrist', 'left_hip', 'right_hip',
    'left_knee', 'right_knee', 'left_ankle', 'right_ankle'
]
# List of keys from arm and leg rules
ARM_KEYS = ['arm_position', 'left_arm_position', 'right_arm_position']
LEG_KEYS = ['leg_position', 'left_leg_position', 'right_leg_position']
# List of keys from specific exercise rules
EXERCISE_KEYS = [
        'posture',
        'arm_position',
        'leg_position',
        'exercise_specific'
    ]
# Threshold constants for position detection (e.g., distances in pixels or units used)
CLOSE = 10          # Threshold to determine if two points are 'close' to each other
SPREAD = 50         # Threshold to determine if arms are 'spread' apart

# Constants for angle thresholds (in degrees)
STRAIGHT = 8                        # Degrees; threshold to consider a limb 'straight'
HIP_HINGE_ANGLE_THRESHOLD = 30      # Degrees; threshold for detecting 'hip_hinge' posture

# Constants for posture detection (distance thresholds)
STANDING = 20                       # Vertical distance threshold for 'standing' posture
UPRIGHT = 15                        # Vertical distance threshold for 'upright' posture
BENT = 40                           # Vertical distance threshold for 'bent' posture

# Constant for core engagement detection (distance threshold)
CORE_ENGAGEMENT_THRESHOLD = 50      # Threshold for detecting 'core_engaged' posture
