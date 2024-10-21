# main.py
import sys
sys.path.insert(0, './yolov7')
#sys.path.insert(0, './RuleExtraction/yolov7')
from helper import  *
from constants import *
from exercise_rules import *
from process_video import process_video
from GYMDetector import YOLOv7EquipmentDetector,PoseDetector
import os
import json


def compare_joint_positions(
    actual_rules: dict,
    expected_rules: dict
) -> float:
    matched = calculate_match(actual_rules,expected_rules)
    return matched

# def main():
video_root_dir = "../blender_mp4/"
#model_path = "home/bizon/dong/yolov7/best-v2.pt"
model_path = "./assets/best-v2.pt"

equipment_detector = YOLOv7EquipmentDetector(model_path, EQUIPMENTS)
pose_detector = PoseDetector()

exercises_rules = build_exercise_rules_json()
exercises_names = get_exercise_names(exercises_rules)
rules_dict, equipment_dict, other_dict = build_rule_dict(exercises_rules)

video_list,target_exercise_names = get_video_path(video_root_dir,exercises_names)
target_rules_dict, target_eqp_dict, target_other_dict = get_sub_rules_for_activities(target_exercise_names,rules_dict, equipment_dict, other_dict)
results = []

video_count =0
for video,activity in zip(video_list,target_exercise_names):
    video_count+=1
    print(f"Processing video #{video_count}: {video}")
    target_rule = target_rules_dict[activity]
    
    target_equipment = target_eqp_dict[activity]
    target_other = target_other_dict[activity]
    print(target_rule)
    curr_pose_dict,curr_equipmnet_dict,curr_other_dict = process_video(equipment_detector,pose_detector,video,log_to_file=True)
    print("Detected Poses:", curr_pose_dict)
    print("Detected equipement:", curr_equipmnet_dict)
    print("Other: ", curr_other_dict)

# if __name__ =="__main__":
#     main()




# def process_exercise(description: str,video_path) -> None:
#     #joint_positions = get_joint_positions_from_video()  # Simulate joint position extraction
#     joint_positions_overtime = get_joint_positions_from_video(video_path)
#     actual_rules = {}
#     expected_rules = parse_exercise_description(description)  # Parse expected rules from description
#     for joint_positions in joint_positions_overtime:
#         new_rules = generate_joint_rules(joint_positions)  # Generate rules based on actual positions
#         for key,value in new_rules.items():
#             if key in actual_rules:
#                 actual_rules[key].append(value)
#             else:
#                 actual_rules[key] = value
#     print("\nActual Rules:")
#     for key, value in actual_rules.items():
#         print(f"{key}: {value}")

#     print("\nExpected Rules:")
#     for key, value in expected_rules.items():
#         print(f"{key}: {value}")

#     matched = compare_joint_positions(actual_rules, expected_rules)

#     if matched>MATCH_THRESHOLD:
#         print("\nExercise performed correctly.")
#     else:
#             print("\nExercise performance did not match the description.")

# Example usage for the specific kettlebell exercise
# TEST_PATH = "../test_json"
# gpt_rules = {}
# for filename in os.listdir(TEST_PATH):
#     base_name = os.path.splitext(filename)[0]
#     currpath = os.path.join(TEST_PATH,filename)
#     with open(currpath,'r') as file:
#         data = json.load(file)
#         gpt_rules[base_name] = data
#     file.close()
#print(gpt_rules)
