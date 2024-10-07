#exercise_rules
# try manual extraction of rules for 30 exececises
# in the format of list of json
def build_rule_dict(rules):
    body_landmarks_dict = {}
    equipment_dict = {}
    other_dict = {}
    # Iterate through the list of exercise rules
    for rule in rules:
        activity_name = rule.get("activity", "").strip().lower()

        if activity_name:  # Ensure the activity name is not empty
            body_landmarks_dict[activity_name] = rule.get("body_landmarks", {})
            equipment_dict[activity_name] = rule.get("equipment", {})
            other_dict[activity_name] = rule.get("other",{})
    return body_landmarks_dict, equipment_dict, other_dict

def get_sub_rules_for_activities(activities: list, body: dict, equipment:dict, other: dict) -> tuple:
    body_sub_rules = {}
    equipment_sub_rules = {}
    other_subrules = {}

    for activity in activities:
        if activity in body and activity in equipment and activity in other:
            body_sub_rules[activity] = body[activity]
            equipment_sub_rules[activity] = equipment[activity]
            other_subrules[activity] = other[activity]
        else:
            raise ValueError(f"Activity '{activity}' not found in the rules.")

    return body_sub_rules,equipment_sub_rules,other_subrules

def get_exercise_names(json_rules)-> list:
    name_set = set()
    for exercise in json_rules:
        try:
            curr = exercise.get("activity","").strip().lower()
            if curr:
                if curr in name_set:
                    raise ValueError(f"Duplication activity found: {curr}")
                name_set.add(curr)
        except ValueError as ve:
            print(ve)
    return list(name_set)  

def build_exercise_rules_json() -> list:
    exercise_rules = [
        {
            "activity": "Dumbbell Bench Press",
            "body_landmarks": {
                "left_foot": {
                    "position": [ "flat","on ground"],
                    "motion": ["stationary"]
                },
                "right_foot": {
                    "position": ["flat","on ground"],
                    "motion": ["stationary"]
                },
                "left_hip": {
                    "position": ["seated"],
                    "motion": ["stationary"]
                },
                "right_hip": {
                    "position": ["seated"],
                    "motion": ["stationary"]
                },
                "torso": {
                    "position": ["neutral spine", "on bench"],
                    "motion": ["stationary"]
                },
                "left_hand": {
                    "position": ["holding equipment","vertical upward"],
                    "motion": ["horizontal outward","horizontal inward","vertical upward","vertical downward"]
                },
                "right_hand": {
                    "position": ["holding equipment","vertical upward"],
                    "motion": ["horizontal outward","horizontal inward","vertical upward","vertical downward"]
                },
                "left_elbow": {
                    "position": ["slightly flexed"],
                    "motion": ["extension", "flexion"]
                },
                "right_elbow": {
                    "position": ["slightly flexed"],
                    "motion": ["extension","flexsion"]
                },
                "left_shoulder": {
                    "position": ["on bench", "retracted"],
                    "motion": ["stationary"]
                },
                "right_shoulder": {
                    "position": ["on bench", "retracted"],
                    "motion": ["stationary"]
                },
                "left_knee": {
                    "position": ["bent at 90 degrees"],
                    "motion": ["stationary"]
                },
                "right_knee": {
                    "position": ["bent at 90 degrees"],
                    "motion": ["stationary"]
                }
            },
            "equipment": {
                "type": ["bench","dumbbell"],
                "bench incline":["45"]
            },
            "other":{
                "mirrored":"true"
            }
        },
        {
            "activity": "Dumbbell Alternating Pendlay Row",
            "body_landmarks": {
                "left_foot": {
                    "position": ["shoulder-width apart","flat","on ground"],
                    "motion": ["stationary"]
                },
                "right_foot": {
                    "position": ["shoulder-width apart","flat","on ground"],
                    "motion": ["stationary"]
                },
                "left_hip": {
                    "position": ["hip hinge"],
                    "motion": ["stationary"]
                },
                "right_hip": {
                    "position": ["hip hinge"],
                    "motion": ["stationary"]
                },
                "torso": {
                    "position": ["leaning forward", "neutral spine"],
                    "motion": ["stationary"]
                },
                "left_hand": {
                    "position": ["holding equipment","vertical downward"],
                    "motion": ["row","vertical upward","vertical downward","stationary"]
                },
                "right_hand": {
                    "position": ["holding equipment","vertical downward"],
                    "motion": ["row","vertical upward","vertical downward","stationary"]
                },
                "left_elbow": {
                    "position": ["extended","flexed"],
                    "motion": ["flexion","extension"]
                },
                "right_elbow": {
                    "position": ["extended","flexed"],
                    "motion": ["flexion","extension"]
                },
                "left_shoulder": {
                    "position": ["neutral"],
                    "motion": ["stationary"]
                },
                "right_shoulder": {
                    "position": ["neutral"],
                    "motion": ["stationary"]
                },
                "left_knee": {
                    "position": ["bent"],
                    "motion": ["stationary"]
                },
                "right_knee": {
                    "position": ["bent"],
                    "motion": ["stationary"]
                }
            },
            "equipment": {
                "type": ["dumbbell"],
                "bench incline":["none"]
            },
            "other":{
                "mirrored":"false"
            }
        },
        {
            "activity": "Dumbbell Bulgarian Split Squat",
            "body_landmarks": {
                "left_foot": {
                    "position": ["flat","on bench", "on ground"],
                    "motion": ["vertical upward","vertical downward","stationary"]
                },
                "right_foot": {
                    "position": ["flat","on bench", "on ground"],
                    "motion": ["vertical upward","vertical downward","stationary"]
                },
                "left_hip": {
                    "position": ["neutral"],
                    "motion": ["vertical upward","vertical downward"]
                },
                "right_hip": {
                    "position": ["neutral"],
                    "motion": ["vertical upward","vertical downward"]
                },
                "torso": {
                    "position": ["upright", "slightly leaning forward"],
                    "motion": ["vertical upward","vertical downward"]
                },
                "left_hand": {
                    "position": ["holding equipment", "vertical downward"],
                    "motion": ["vertical upward","vertical downward"]
                },
                "right_hand": {
                    "position": ["holding equipment", "vertical downward"],
                    "motion": ["vertical upward","vertical downward"]
                },
                "left_elbow": {
                    "position": ["extended"],
                    "motion": ["stationary"]
                },
                "right_elbow": {
                    "position": ["extended"],
                    "motion": ["stationary"]
                },
                "left_shoulder": {
                    "position": ["neutral"],
                    "motion": ["vertical upward","vertical downward"]
                },
                "right_shoulder": {
                    "position": ["neutral"],
                    "motion": ["vertical upward","vertical downward"]
                },
                "left_knee": {
                    "position": ["flexed","bent"],
                    "motion": ["extention","flexion"]
                },
                "right_knee": {
                    "position": ["flexed","bent"],
                    "motion": ["extention","flexion"]
                }
            },
            "equipment": {
                "type": ["bumbbell","bench"],
                "bench incline":["0"]
            },
            "other":{
                "mirrored":"false"
            }
        },
        {
            "activity": "Dumbbell Calf Raise",
            "body_landmarks": {
                "left_foot": {
                    "position": ["flat", "on ground"],
                    "motion": ["stationary","plantar flexion"]
                },
                "right_foot": {
                    "position": ["flat", "on ground"],
                    "motion": ["stationary","plantar flexion"]
                },
                "left_hip": {
                    "position": ["neutral"],
                    "motion": ["stationary"]
                },
                "right_hip": {
                    "position": ["neutral"],
                    "motion": ["stationary"]
                },
                "torso": {
                    "position": ["upright","neutral spine"],
                    "motion": ["stationary","vertical upward","vertical downward"]
                },
                "left_hand": {
                    "position": ["holding equipment","vertical downward"],
                    "motion": ["stationary","vertical upward","vertical downward"]
                },
                "right_hand": {
                    "position": ["holding equipment","vertical downward"],
                    "motion": ["stationary","vertical upward","vertical downward"]
                },
                "left_elbow": {
                    "position": ["extended"],
                    "motion": ["stationary"]
                },
                "right_elbow": {
                    "position": ["extended"],
                    "motion": ["stationary"]
                },
                "left_shoulder": {
                    "position": ["neutral"],
                    "motion": ["stationary","vertical upward","vertical downward"]
                },
                "right_shoulder": {
                    "position": ["neutral"],
                    "motion": ["stationary","vertical upward","vertical downward"]
                },
                "left_knee": {
                    "position": ["extended"],
                    "motion": ["stationary"]
                },
                "right_knee": {
                    "position": ["extended"],
                    "motion": ["stationary"]
                }
            },
            "equipment": {
                "type": ["dumbbell"],
                "bench incline":["none"]
            },
            "other":{
                "mirrored":"true"
            }
        },
        {
            "activity": "Dumbbell Chest Fly",
            "body_landmarks": {
                "left_foot": {
                    "position": [ "flat","on ground"],
                    "motion": ["stationary"]
                },
                "right_foot": {
                    "position": ["flat","on ground"],
                    "motion": ["stationary"]
                },
                "left_hip": {
                    "position": ["seated"],
                    "motion": ["stationary"]
                },
                "right_hip": {
                    "position": ["seated"],
                    "motion": ["stationary"]
                },
                "torso": {
                    "position": ["neutral spine", "on bench"],
                    "motion": ["stationary"]
                },
                "left_hand": {
                    "position": ["holding equipment","vertical upward"],
                    "motion": ["horizontal outward","horizontal inward","vertical upward","vertical downward"]
                },
                "right_hand": {
                    "position": ["holding equipment","vertical upward"],
                    "motion": ["horizontal outward","horizontal inward","vertical upward","vertical downward"]
                },
                "left_elbow": {
                    "position": ["slightly flexed","bent"],
                    "motion": ["extension", "flexion"]
                },
                "right_elbow": {
                    "position": ["slightly flexed","bent"],
                    "motion": ["extension","flexsion"]
                },
                "left_shoulder": {
                    "position": ["on bench", "retracted"],
                    "motion": ["stationary"]
                },
                "right_shoulder": {
                    "position": ["on bench", "retracted"],
                    "motion": ["stationary"]
                },
                "left_knee": {
                    "position": ["bent at 90 degrees"],
                    "motion": ["stationary"]
                },
                "right_knee": {
                    "position": ["bent at 90 degrees"],
                    "motion": ["stationary"]
                }
            },
            "equipment": {
                "type": ["bench","dumbbell"],
                "bench incline":["0"]
            },
            "other":{
                "mirrored":"true"
            }
        },
        {
            "activity": "Dumbbell Curl",
            "body_landmarks": {
                "left_foot": {
                    "position": ["shoulder-width apart","flat","on ground"],
                    "motion": ["stationary"]
                },
                "right_foot": {
                    "position": ["shoulder-width apart","flat","on ground"],
                    "motion": ["stationary"]
                },
                "left_hip": {
                    "position": ["hip hinge"],
                    "motion": ["stationary"]
                },
                "right_hip": {
                    "position": ["hip hinge"],
                    "motion": ["stationary"]
                },
                "torso": {
                    "position": ["leaning forward", "neutral spine"],
                    "motion": ["stationary"]
                },
                "torso": {
                    "position": ["upright","neutral spine"],
                    "motion": ["stationary"]
                },
                "left_hand": {
                    "position": ["holding equipment"],
                    "motion": ["vertical upward","vertical downward"]
                },
                "right_hand": {
                    "position": ["holding equipment"],
                    "motion": ["vertical upward","vertical downward"]
                },
                "left_elbow": {
                    "position": ["flexed","extended","close to torso"],
                    "motion": ["extention,flexion"]
                },
                "right_elbow": {
                    "position": ["flexed","extended","close to torso"],
                    "motion": ["extention,flexion"]
                },
                "left_shoulder": {
                    "position": ["neutral"],
                    "motion": ["stationary"]
                },
                "right_shoulder": {
                    "position": ["neutral"],
                    "motion": ["stationary"]
                },
                "left_knee": {
                    "position": ["slightly bent"],
                    "motion": ["stationary"]
                },
                "right_knee": {
                    "position": ["slightly bent"],
                    "motion": ["stationary"]
                }
            },
            "equipment": {
                "type": ["dumbbell"],
                "bench incline":["none"]
            },
            "other":{
                "mirrored":"true"
            }
        },
        {
            "activity": "Dumbbell Decline Chest Press",
            "body_landmarks": {
                "left_foot": {
                    "position": [ "flat","on ground"],
                    "motion": ["stationary"]
                },
                "right_foot": {
                    "position": ["flat","on ground"],
                    "motion": ["stationary"]
                },
                "left_hip": {
                    "position": ["seated"],
                    "motion": ["stationary"]
                },
                "right_hip": {
                    "position": ["seated"],
                    "motion": ["stationary"]
                },
                "torso": {
                    "position": ["neutral spine", "on bench"],
                    "motion": ["stationary"]
                },
                "left_hand": {
                    "position": ["holding equipment","vertical upward"],
                    "motion": ["vertical upward","vertical downward"]
                },
                "right_hand": {
                    "position": ["holding equipment","vertical upward"],
                    "motion": ["vertical upward","vertical downward"]
                },
                "left_elbow": {
                    "position": ["slightly flexed","bent"],
                    "motion": ["extension", "flexion"]
                },
                "right_elbow": {
                    "position": ["slightly flexed","bent"],
                    "motion": ["extension","flexsion"]
                },
                "left_shoulder": {
                    "position": ["on bench", "retracted"],
                    "motion": ["stationary"]
                },
                "right_shoulder": {
                    "position": ["on bench", "retracted"],
                    "motion": ["stationary"]
                },
                "left_knee": {
                    "position": ["bent at 90 degrees"],
                    "motion": ["stationary"]
                },
                "right_knee": {
                    "position": ["bent at 90 degrees"],
                    "motion": ["stationary"]
                }
            },
            "equipment": {
                "type": ["bench","dumbbell"],
                "bench incline":["0"]
            },
            "other":{
                "mirrored":"true"
            }
        },
        {
            "activity": "Dumbbell Decline Guillotine Bench Press",
            "body_landmarks": {
                "left_foot": {
                    "position": [ "flat","on ground"],
                    "motion": ["stationary"]
                },
                "right_foot": {
                    "position": ["flat","on ground"],
                    "motion": ["stationary"]
                },
                "left_hip": {
                    "position": ["seated"],
                    "motion": ["stationary"]
                },
                "right_hip": {
                    "position": ["seated"],
                    "motion": ["stationary"]
                },
                "torso": {
                    "position": ["neutral spine", "on bench"],
                    "motion": ["stationary"]
                },
                "left_hand": {
                    "position": ["over chest","holding equipment","vertical upward"],
                    "motion": ["vertical upward","vertical downward"]
                },
                "right_hand": {
                    "position": ["over chest","holding equipment","vertical upward"],
                    "motion": ["vertical upward","vertical downward"]
                },
                "left_elbow": {
                    "position": ["slightly flexed","bent"],
                    "motion": ["extension", "flexion"]
                },
                "right_elbow": {
                    "position": ["slightly flexed","bent"],
                    "motion": ["extension","flexsion"]
                },
                "left_shoulder": {
                    "position": ["on bench", "retracted","protracted"],
                    "motion": ["scapular protraction","scapular retraction"]
                },
                "right_shoulder": {
                    "position": ["on bench", "retracted","protracted"],
                    "motion": ["scapular protraction","scapular retraction"]

                },
                "left_knee": {
                    "position": ["bent at 90 degrees"],
                    "motion": ["stationary"]
                },
                "right_knee": {
                    "position": ["bent at 90 degrees"],
                    "motion": ["stationary"]
                }
            },
            "equipment": {
                "type": ["bench","dumbbell"],
                "bench incline":["0"]
            },
            "other":{
                "mirrored":"true"
            }
        },
        {
            "activity": "Dumbbell Decline Single Arm Bench Press",
            "body_landmarks": {
                "left_foot": {
                    "position": [ "flat","on ground"],
                    "motion": ["stationary"]
                },
                "right_foot": {
                    "position": ["flat","on ground"],
                    "motion": ["stationary"]
                },
                "left_hip": {
                    "position": ["seated"],
                    "motion": ["stationary"]
                },
                "right_hip": {
                    "position": ["seated"],
                    "motion": ["stationary"]
                },
                "torso": {
                    "position": ["neutral spine", "on bench"],
                    "motion": ["stationary"]
                },
                "left_hand": {
                    "position": ["holding equipment","vertical upward"],
                    "motion": ["horizontal outward","horizontal inward","vertical upward","vertical downward"]
                },
                "right_hand": {
                    "position": ["holding equipment","vertical upward"],
                    "motion": ["horizontal outward","horizontal inward","vertical upward","vertical downward"]
                },
                "left_elbow": {
                    "position": ["slightly flexed"],
                    "motion": ["extension", "flexion"]
                },
                "right_elbow": {
                    "position": ["slightly flexed"],
                    "motion": ["extension","flexsion"]
                },
                "left_shoulder": {
                    "position": ["on bench", "retracted"],
                    "motion": ["stationary"]
                },
                "right_shoulder": {
                    "position": ["on bench", "retracted"],
                    "motion": ["stationary"]
                },
                "left_knee": {
                    "position": ["bent at 90 degrees"],
                    "motion": ["stationary"]
                },
                "right_knee": {
                    "position": ["bent at 90 degrees"],
                    "motion": ["stationary"]
                }
            },
            "equipment": {
                "type": ["bench","dumbbell"],
                "bench incline":["0"]
            },
            "other":{
                "mirrored":"false"
            }
        },
        {
            "activity": "Dumbbell Decline Skullcrusher",
            "body_landmarks": {
                "left_foot": {
                    "position": [ "flat","on ground"],
                    "motion": ["stationary"]
                },
                "right_foot": {
                    "position": ["flat","on ground"],
                    "motion": ["stationary"]
                },
                "left_hip": {
                    "position": ["seated"],
                    "motion": ["stationary"]
                },
                "right_hip": {
                    "position": ["seated"],
                    "motion": ["stationary"]
                },
                "torso": {
                    "position": ["neutral spine", "on bench"],
                    "motion": ["stationary"]
                },
                "left_hand": {
                    "position": ["over head","over chest","holding equipment","vertical upward"],
                    "motion": ["vertical upward","vertical downward"]
                },
                "right_hand": {
                    "position": ["over head","over chest","holding equipment","vertical upward"],
                    "motion": ["vertical upward","vertical downward"]
                },
                "left_elbow": {
                    "position": ["slightly flexed"],
                    "motion": ["stationary"]
                },
                "right_elbow": {
                   "position": ["slightly flexed"],
                    "motion": ["stationary"]
                },
                "left_shoulder": {
                    "position": ["on bench", "retracted"],
                    "motion": ["flexion","extension"]
                },
                "right_shoulder": {
                    "position": ["on bench", "retracted"],
                    "motion": ["flexion","extension"]
                },
                "left_knee": {
                    "position": ["bent at 90 degrees"],
                    "motion": ["stationary"]
                },
                "right_knee": {
                    "position": ["bent at 90 degrees"],
                    "motion": ["stationary"]
                }
            },
            "equipment": {
                "type": ["bench","dumbbell"],
                "bench incline":["0"]
            },
            "other":{
                "mirrored":"true"
            }
        },
        {
            "activity": "",
            "body_landmarks": {
                "left_foot": {
                    "position": [],
                    "motion": []
                },
                "right_foot": {
                    "position": [],
                    "motion": []
                },
                "left_hip": {
                    "position": [],
                    "motion": []
                },
                "right_hip": {
                    "position": [],
                    "motion": []
                },
                "torso": {
                    "position": [],
                    "motion": []
                },
                "left_hand": {
                    "position": [],
                    "motion": []
                },
                "right_hand": {
                    "position": [],
                    "motion": []
                },
                "left_elbow": {
                    "position": [],
                    "motion": []
                },
                "right_elbow": {
                    "position": [],
                    "motion": []
                },
                "left_shoulder": {
                    "position": [],
                    "motion": []
                },
                "right_shoulder": {
                    "position": [],
                    "motion": []
                },
                "left_knee": {
                    "position": [],
                    "motion": []
                },
                "right_knee": {
                    "position": [],
                    "motion": []
                }
            },
            "equipment": {
                "type": [],
                "bench incline":["none"]
            },
            "other":{
                "mirrored":"false"
            }
        },
        {
            "activity": "",
            "body_landmarks": {
                "left_foot": {
                    "position": [],
                    "motion": []
                },
                "right_foot": {
                    "position": [],
                    "motion": []
                },
                "left_hip": {
                    "position": [],
                    "motion": []
                },
                "right_hip": {
                    "position": [],
                    "motion": []
                },
                "torso": {
                    "position": [],
                    "motion": []
                },
                "left_hand": {
                    "position": [],
                    "motion": []
                },
                "right_hand": {
                    "position": [],
                    "motion": []
                },
                "left_elbow": {
                    "position": [],
                    "motion": []
                },
                "right_elbow": {
                    "position": [],
                    "motion": []
                },
                "left_shoulder": {
                    "position": [],
                    "motion": []
                },
                "right_shoulder": {
                    "position": [],
                    "motion": []
                },
                "left_knee": {
                    "position": [],
                    "motion": []
                },
                "right_knee": {
                    "position": [],
                    "motion": []
                }
            },
            "equipment": {
                "type": [],
                "bench incline":["none"]
            },
            "other":{
                "mirrored":"false"
            }
        },#TODO
        {
            "activity": "Dumbbell Decline Squeeze Press",
            "body_landmarks": {
                "left_foot": {
                    "position": [],
                    "motion": []
                },
                "right_foot": {
                    "position": [],
                    "motion": []
                },
                "left_hip": {
                    "position": [],
                    "motion": []
                },
                "right_hip": {
                    "position": [],
                    "motion": []
                },
                "torso": {
                    "position": [],
                    "motion": []
                },
                "left_hand": {
                    "position": [],
                    "motion": []
                },
                "right_hand": {
                    "position": [],
                    "motion": []
                },
                "left_elbow": {
                    "position": [],
                    "motion": []
                },
                "right_elbow": {
                    "position": [],
                    "motion": []
                },
                "left_shoulder": {
                    "position": [],
                    "motion": []
                },
                "right_shoulder": {
                    "position": [],
                    "motion": []
                },
                "left_knee": {
                    "position": [],
                    "motion": []
                },
                "right_knee": {
                    "position": [],
                    "motion": []
                }
            },
            "equipment": {
                "type": [],
                "bench incline":["none"]
            },
            "other":{
                "mirrored":"false"
            }
        },{
            "activity": "Dumbbell Figure Four Glute Bridge",
            "body_landmarks": {
                "left_foot": {
                    "position": [],
                    "motion": []
                },
                "right_foot": {
                    "position": [],
                    "motion": []
                },
                "left_hip": {
                    "position": [],
                    "motion": []
                },
                "right_hip": {
                    "position": [],
                    "motion": []
                },
                "torso": {
                    "position": [],
                    "motion": []
                },
                "left_hand": {
                    "position": [],
                    "motion": []
                },
                "right_hand": {
                    "position": [],
                    "motion": []
                },
                "left_elbow": {
                    "position": [],
                    "motion": []
                },
                "right_elbow": {
                    "position": [],
                    "motion": []
                },
                "left_shoulder": {
                    "position": [],
                    "motion": []
                },
                "right_shoulder": {
                    "position": [],
                    "motion": []
                },
                "left_knee": {
                    "position": [],
                    "motion": []
                },
                "right_knee": {
                    "position": [],
                    "motion": []
                }
            },
            "equipment": {
                "type": [],
                "bench incline":["none"]
            },
            "other":{
                "mirrored":"false"
            }
        },
        {
            "activity": "Dumbbell Figure Four Hip Thrust",
            "body_landmarks": {
                "left_foot": {
                    "position": [],
                    "motion": []
                },
                "right_foot": {
                    "position": [],
                    "motion": []
                },
                "left_hip": {
                    "position": [],
                    "motion": []
                },
                "right_hip": {
                    "position": [],
                    "motion": []
                },
                "torso": {
                    "position": [],
                    "motion": []
                },
                "left_hand": {
                    "position": [],
                    "motion": []
                },
                "right_hand": {
                    "position": [],
                    "motion": []
                },
                "left_elbow": {
                    "position": [],
                    "motion": []
                },
                "right_elbow": {
                    "position": [],
                    "motion": []
                },
                "left_shoulder": {
                    "position": [],
                    "motion": []
                },
                "right_shoulder": {
                    "position": [],
                    "motion": []
                },
                "left_knee": {
                    "position": [],
                    "motion": []
                },
                "right_knee": {
                    "position": [],
                    "motion": []
                }
            },
            "equipment": {
                "type": ["dumbbell","bench"],
                "bench incline":["0"]
            },
            "other":{
                "mirrored":"false"
            }
        },{
            "activity": "Dumbbell Forward Lunge",
            "body_landmarks": {
                "left_foot": {
                    "position": [],
                    "motion": []
                },
                "right_foot": {
                    "position": [],
                    "motion": []
                },
                "left_hip": {
                    "position": [],
                    "motion": []
                },
                "right_hip": {
                    "position": [],
                    "motion": []
                },
                "torso": {
                    "position": [],
                    "motion": []
                },
                "left_hand": {
                    "position": [],
                    "motion": []
                },
                "right_hand": {
                    "position": [],
                    "motion": []
                },
                "left_elbow": {
                    "position": [],
                    "motion": []
                },
                "right_elbow": {
                    "position": [],
                    "motion": []
                },
                "left_shoulder": {
                    "position": [],
                    "motion": []
                },
                "right_shoulder": {
                    "position": [],
                    "motion": []
                },
                "left_knee": {
                    "position": [],
                    "motion": []
                },
                "right_knee": {
                    "position": [],
                    "motion": []
                }
            },
            "equipment": {
                "type": ["Dumbbell"],
                "bench incline":["none"]
            },
            "other":{
                "mirrored":"false"
            }
        },
        {
            "activity": "Dumbbell Front Rack Pause Squat",
            "body_landmarks": {
                "left_foot": {
                    "position": [],
                    "motion": []
                },
                "right_foot": {
                    "position": [],
                    "motion": []
                },
                "left_hip": {
                    "position": [],
                    "motion": []
                },
                "right_hip": {
                    "position": [],
                    "motion": []
                },
                "torso": {
                    "position": [],
                    "motion": []
                },
                "left_hand": {
                    "position": [],
                    "motion": []
                },
                "right_hand": {
                    "position": [],
                    "motion": []
                },
                "left_elbow": {
                    "position": [],
                    "motion": []
                },
                "right_elbow": {
                    "position": [],
                    "motion": []
                },
                "left_shoulder": {
                    "position": [],
                    "motion": []
                },
                "right_shoulder": {
                    "position": [],
                    "motion": []
                },
                "left_knee": {
                    "position": [],
                    "motion": []
                },
                "right_knee": {
                    "position": [],
                    "motion": []
                }
            },
            "equipment": {
                "type": ["Dumbbell"],
                "bench incline":["none"]
            },
            "other":{
                "mirrored":"false"
            }
        },
        {
            "activity": "Dumbbell Front Raise",
            "body_landmarks": {
                "left_foot": {
                    "position": [],
                    "motion": []
                },
                "right_foot": {
                    "position": [],
                    "motion": []
                },
                "left_hip": {
                    "position": [],
                    "motion": []
                },
                "right_hip": {
                    "position": [],
                    "motion": []
                },
                "torso": {
                    "position": [],
                    "motion": []
                },
                "left_hand": {
                    "position": [],
                    "motion": []
                },
                "right_hand": {
                    "position": [],
                    "motion": []
                },
                "left_elbow": {
                    "position": [],
                    "motion": []
                },
                "right_elbow": {
                    "position": [],
                    "motion": []
                },
                "left_shoulder": {
                    "position": [],
                    "motion": []
                },
                "right_shoulder": {
                    "position": [],
                    "motion": []
                },
                "left_knee": {
                    "position": [],
                    "motion": []
                },
                "right_knee": {
                    "position": [],
                    "motion": []
                }
            },
            "equipment": {
                "type": ["Dumbbell"],
                "bench incline":["none"]
            },
            "other":{
                "mirrored":"false"
            }
        },{
            "activity": "Dumbbell Glute Bridge",
            "body_landmarks": {
                "left_foot": {
                    "position": [],
                    "motion": []
                },
                "right_foot": {
                    "position": [],
                    "motion": []
                },
                "left_hip": {
                    "position": [],
                    "motion": []
                },
                "right_hip": {
                    "position": [],
                    "motion": []
                },
                "torso": {
                    "position": [],
                    "motion": []
                },
                "left_hand": {
                    "position": [],
                    "motion": []
                },
                "right_hand": {
                    "position": [],
                    "motion": []
                },
                "left_elbow": {
                    "position": [],
                    "motion": []
                },
                "right_elbow": {
                    "position": [],
                    "motion": []
                },
                "left_shoulder": {
                    "position": [],
                    "motion": []
                },
                "right_shoulder": {
                    "position": [],
                    "motion": []
                },
                "left_knee": {
                    "position": [],
                    "motion": []
                },
                "right_knee": {
                    "position": [],
                    "motion": []
                }
            },
            "equipment": {
                "type": ["Dumbbell"],
                "bench incline":["none"]
            },
            "other":{
                "mirrored":"false"
            }
        },{
            "activity": "Kettlebell calf Raises",
            "body_landmarks": {
                "left_foot": {
                    "position": [],
                    "motion": []
                },
                "right_foot": {
                    "position": [],
                    "motion": []
                },
                "left_hip": {
                    "position": [],
                    "motion": []
                },
                "right_hip": {
                    "position": [],
                    "motion": []
                },
                "torso": {
                    "position": [],
                    "motion": []
                },
                "left_hand": {
                    "position": [],
                    "motion": []
                },
                "right_hand": {
                    "position": [],
                    "motion": []
                },
                "left_elbow": {
                    "position": [],
                    "motion": []
                },
                "right_elbow": {
                    "position": [],
                    "motion": []
                },
                "left_shoulder": {
                    "position": [],
                    "motion": []
                },
                "right_shoulder": {
                    "position": [],
                    "motion": []
                },
                "left_knee": {
                    "position": [],
                    "motion": []
                },
                "right_knee": {
                    "position": [],
                    "motion": []
                }
            },
            "equipment": {
                "type": ["Kettlebell"],
                "bench incline":["none"]
            },
            "other":{
                "mirrored":"false"
            }
        },{
            "activity": "Kettlebell Chest Press",
            "body_landmarks": {
                "left_foot": {
                    "position": [ "flat","on ground"],
                    "motion": ["stationary"]
                },
                "right_foot": {
                    "position": ["flat","on ground"],
                    "motion": ["stationary"]
                },
                "left_hip": {
                    "position": ["seated"],
                    "motion": ["stationary"]
                },
                "right_hip": {
                    "position": ["seated"],
                    "motion": ["stationary"]
                },
                "torso": {
                    "position": ["neutral spine", "on bench"],
                    "motion": ["stationary"]
                },
                "left_hand": {
                    "position": ["holding equipment","vertical upward"],
                    "motion": ["vertical upward","vertical downward"]
                },
                "right_hand": {
                    "position": ["holding equipment","vertical upward"],
                    "motion": ["vertical upward","vertical downward"]
                },
                "left_elbow": {
                    "position": ["slightly flexed","bent"],
                    "motion": ["extension", "flexion"]
                },
                "right_elbow": {
                    "position": ["slightly flexed","bent"],
                    "motion": ["extension","flexsion"]
                },
                "left_shoulder": {
                    "position": ["on bench", "retracted"],
                    "motion": ["stationary"]
                },
                "right_shoulder": {
                    "position": ["on bench", "retracted"],
                    "motion": ["stationary"]
                },
                "left_knee": {
                    "position": ["bent at 90 degrees"],
                    "motion": ["stationary"]
                },
                "right_knee": {
                    "position": ["bent at 90 degrees"],
                    "motion": ["stationary"]
                }
            },
            "equipment": {
                "type": ["bench","kettlebell"],
                "bench incline":["0"]
            },
            "other":{
                "mirrored":"true"
            }
        },{
            "activity": "Kettlebell Concentration Curl",
            "body_landmarks": {
                "left_foot": {
                    "position": [],
                    "motion": []
                },
                "right_foot": {
                    "position": [],
                    "motion": []
                },
                "left_hip": {
                    "position": [],
                    "motion": []
                },
                "right_hip": {
                    "position": [],
                    "motion": []
                },
                "torso": {
                    "position": [],
                    "motion": []
                },
                "left_hand": {
                    "position": [],
                    "motion": []
                },
                "right_hand": {
                    "position": [],
                    "motion": []
                },
                "left_elbow": {
                    "position": [],
                    "motion": []
                },
                "right_elbow": {
                    "position": [],
                    "motion": []
                },
                "left_shoulder": {
                    "position": [],
                    "motion": []
                },
                "right_shoulder": {
                    "position": [],
                    "motion": []
                },
                "left_knee": {
                    "position": [],
                    "motion": []
                },
                "right_knee": {
                    "position": [],
                    "motion": []
                }
            },
            "equipment": {
                "type": [],
                "bench incline":["none"]
            },
            "other":{
                "mirrored":"false"
            }
        },{
            "activity": "Kettlebell Deadlift",
            "body_landmarks": {
                "left_foot": {
                    "position": [],
                    "motion": []
                },
                "right_foot": {
                    "position": [],
                    "motion": []
                },
                "left_hip": {
                    "position": [],
                    "motion": []
                },
                "right_hip": {
                    "position": [],
                    "motion": []
                },
                "torso": {
                    "position": [],
                    "motion": []
                },
                "left_hand": {
                    "position": [],
                    "motion": []
                },
                "right_hand": {
                    "position": [],
                    "motion": []
                },
                "left_elbow": {
                    "position": [],
                    "motion": []
                },
                "right_elbow": {
                    "position": [],
                    "motion": []
                },
                "left_shoulder": {
                    "position": [],
                    "motion": []
                },
                "right_shoulder": {
                    "position": [],
                    "motion": []
                },
                "left_knee": {
                    "position": [],
                    "motion": []
                },
                "right_knee": {
                    "position": [],
                    "motion": []
                }
            },
            "equipment": {
                "type": [],
                "bench incline":["none"]
            },
            "other":{
                "mirrored":"false"
            }
        },{
            "activity": "Kettlebell Decline Skull Crusher",
            "body_landmarks": {
                "left_foot": {
                    "position": [],
                    "motion": []
                },
                "right_foot": {
                    "position": [],
                    "motion": []
                },
                "left_hip": {
                    "position": [],
                    "motion": []
                },
                "right_hip": {
                    "position": [],
                    "motion": []
                },
                "torso": {
                    "position": [],
                    "motion": []
                },
                "left_hand": {
                    "position": [],
                    "motion": []
                },
                "right_hand": {
                    "position": [],
                    "motion": []
                },
                "left_elbow": {
                    "position": [],
                    "motion": []
                },
                "right_elbow": {
                    "position": [],
                    "motion": []
                },
                "left_shoulder": {
                    "position": [],
                    "motion": []
                },
                "right_shoulder": {
                    "position": [],
                    "motion": []
                },
                "left_knee": {
                    "position": [],
                    "motion": []
                },
                "right_knee": {
                    "position": [],
                    "motion": []
                }
            },
            "equipment": {
                "type": [],
                "bench incline":["none"]
            },
            "other":{
                "mirrored":"false"
            }
        },{
            "activity": "Kettlebell Glute Bridge",
            "body_landmarks": {
                "left_foot": {
                    "position": [],
                    "motion": []
                },
                "right_foot": {
                    "position": [],
                    "motion": []
                },
                "left_hip": {
                    "position": [],
                    "motion": []
                },
                "right_hip": {
                    "position": [],
                    "motion": []
                },
                "torso": {
                    "position": [],
                    "motion": []
                },
                "left_hand": {
                    "position": [],
                    "motion": []
                },
                "right_hand": {
                    "position": [],
                    "motion": []
                },
                "left_elbow": {
                    "position": [],
                    "motion": []
                },
                "right_elbow": {
                    "position": [],
                    "motion": []
                },
                "left_shoulder": {
                    "position": [],
                    "motion": []
                },
                "right_shoulder": {
                    "position": [],
                    "motion": []
                },
                "left_knee": {
                    "position": [],
                    "motion": []
                },
                "right_knee": {
                    "position": [],
                    "motion": []
                }
            },
            "equipment": {
                "type": [],
                "bench incline":["none"]
            },
            "other":{
                "mirrored":"false"
            }
        },{
            "activity": "Kettlebell Goblet Curl",
            "body_landmarks": {
                "left_foot": {
                    "position": [],
                    "motion": []
                },
                "right_foot": {
                    "position": [],
                    "motion": []
                },
                "left_hip": {
                    "position": [],
                    "motion": []
                },
                "right_hip": {
                    "position": [],
                    "motion": []
                },
                "torso": {
                    "position": [],
                    "motion": []
                },
                "left_hand": {
                    "position": [],
                    "motion": []
                },
                "right_hand": {
                    "position": [],
                    "motion": []
                },
                "left_elbow": {
                    "position": [],
                    "motion": []
                },
                "right_elbow": {
                    "position": [],
                    "motion": []
                },
                "left_shoulder": {
                    "position": [],
                    "motion": []
                },
                "right_shoulder": {
                    "position": [],
                    "motion": []
                },
                "left_knee": {
                    "position": [],
                    "motion": []
                },
                "right_knee": {
                    "position": [],
                    "motion": []
                }
            },
            "equipment": {
                "type": [],
                "bench incline":["none"]
            },
            "other":{
                "mirrored":"false"
            }
        },{
            "activity": "Kettlebell Goblet Good Morning",
            "body_landmarks": {
                "left_foot": {
                    "position": [],
                    "motion": []
                },
                "right_foot": {
                    "position": [],
                    "motion": []
                },
                "left_hip": {
                    "position": [],
                    "motion": []
                },
                "right_hip": {
                    "position": [],
                    "motion": []
                },
                "torso": {
                    "position": [],
                    "motion": []
                },
                "left_hand": {
                    "position": [],
                    "motion": []
                },
                "right_hand": {
                    "position": [],
                    "motion": []
                },
                "left_elbow": {
                    "position": [],
                    "motion": []
                },
                "right_elbow": {
                    "position": [],
                    "motion": []
                },
                "left_shoulder": {
                    "position": [],
                    "motion": []
                },
                "right_shoulder": {
                    "position": [],
                    "motion": []
                },
                "left_knee": {
                    "position": [],
                    "motion": []
                },
                "right_knee": {
                    "position": [],
                    "motion": []
                }
            },
            "equipment": {
                "type": [],
                "bench incline":["none"]
            },
            "other":{
                "mirrored":"false"
            }
        },{
            "activity": "Kettlebell Goblet Squat",
            "body_landmarks": {
                "left_foot": {
                    "position": [],
                    "motion": []
                },
                "right_foot": {
                    "position": [],
                    "motion": []
                },
                "left_hip": {
                    "position": [],
                    "motion": []
                },
                "right_hip": {
                    "position": [],
                    "motion": []
                },
                "torso": {
                    "position": [],
                    "motion": []
                },
                "left_hand": {
                    "position": [],
                    "motion": []
                },
                "right_hand": {
                    "position": [],
                    "motion": []
                },
                "left_elbow": {
                    "position": [],
                    "motion": []
                },
                "right_elbow": {
                    "position": [],
                    "motion": []
                },
                "left_shoulder": {
                    "position": [],
                    "motion": []
                },
                "right_shoulder": {
                    "position": [],
                    "motion": []
                },
                "left_knee": {
                    "position": [],
                    "motion": []
                },
                "right_knee": {
                    "position": [],
                    "motion": []
                }
            },
            "equipment": {
                "type": [],
                "bench incline":["none"]
            },
            "other":{
                "mirrored":"false"
            }
        },{
            "activity": "",
            "body_landmarks": {
                "left_foot": {
                    "position": [],
                    "motion": []
                },
                "right_foot": {
                    "position": [],
                    "motion": []
                },
                "left_hip": {
                    "position": [],
                    "motion": []
                },
                "right_hip": {
                    "position": [],
                    "motion": []
                },
                "torso": {
                    "position": [],
                    "motion": []
                },
                "left_hand": {
                    "position": [],
                    "motion": []
                },
                "right_hand": {
                    "position": [],
                    "motion": []
                },
                "left_elbow": {
                    "position": [],
                    "motion": []
                },
                "right_elbow": {
                    "position": [],
                    "motion": []
                },
                "left_shoulder": {
                    "position": [],
                    "motion": []
                },
                "right_shoulder": {
                    "position": [],
                    "motion": []
                },
                "left_knee": {
                    "position": [],
                    "motion": []
                },
                "right_knee": {
                    "position": [],
                    "motion": []
                }
            },
            "equipment": {
                "type": [],
                "bench incline":["none"]
            },
            "other":{
                "mirrored":"false"
            }
        },{
            "activity": "",
            "body_landmarks": {
                "left_foot": {
                    "position": [],
                    "motion": []
                },
                "right_foot": {
                    "position": [],
                    "motion": []
                },
                "left_hip": {
                    "position": [],
                    "motion": []
                },
                "right_hip": {
                    "position": [],
                    "motion": []
                },
                "torso": {
                    "position": [],
                    "motion": []
                },
                "left_hand": {
                    "position": [],
                    "motion": []
                },
                "right_hand": {
                    "position": [],
                    "motion": []
                },
                "left_elbow": {
                    "position": [],
                    "motion": []
                },
                "right_elbow": {
                    "position": [],
                    "motion": []
                },
                "left_shoulder": {
                    "position": [],
                    "motion": []
                },
                "right_shoulder": {
                    "position": [],
                    "motion": []
                },
                "left_knee": {
                    "position": [],
                    "motion": []
                },
                "right_knee": {
                    "position": [],
                    "motion": []
                }
            },
            "equipment": {
                "type": [],
                "bench incline":["none"]
            },
            "other":{
                "mirrored":"false"
            }
        }
    ]
    return exercise_rules