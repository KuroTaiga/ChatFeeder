# exercise_parser.py

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
    if 'hinge at the hips' in description:
        rules['posture'] = 'hip_hinge'

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
    if 'spread the arms' in description or 'arms spread' in description:
        rules['arm_position'] = 'spread'
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


    #Item related exercise:
    #kettlebell: only hold with hands:
    if 'kettlebell' in description:
        if 'close to the chest' in description:
            rules['left_arm_position'] = 'close_to_chest'
            rules['right_arm_position'] = 'close_to_chest'


    return rules
