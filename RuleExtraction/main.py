# main.py
from helper import  get_joint_positions_from_video,calculate_match
from constants import JOINT_KEYS, MATCH_THRESHOLD
from rules_generation import generate_joint_rules
from exercise_parser import parse_exercise_description
import os
import json

# def load_yolov7_model(weights_path, img_size=640):

#     device = select_device('cuda' if torch.cuda.is_available() else 'cpu')

#     model = attempt_load(weights_path, map_location=device)  # Load model

#     stride = int(model.stride.max())  # Get model stride

#     img_size = check_img_size(img_size, s=stride)  # Check image size

#     if device.type != 'cpu':

#         model.half()  # Convert model to half precision if using GPU

#     return model, device, stride, img_size


def compare_joint_positions(
    actual_rules: dict,
    expected_rules: dict
) -> float:
    matched = calculate_match(actual_rules,expected_rules)
    return matched

def process_exercise(description: str,video_path) -> None:
    #joint_positions = get_joint_positions_from_video()  # Simulate joint position extraction
    joint_positions_overtime = get_joint_positions_from_video(video_path)
    actual_rules = {}
    expected_rules = parse_exercise_description(description)  # Parse expected rules from description
    for joint_positions in joint_positions_overtime:
        new_rules = generate_joint_rules(joint_positions)  # Generate rules based on actual positions
        for key,value in new_rules.items():
            if key in actual_rules:
                actual_rules[key].append(value)
            else:
                actual_rules[key] = value
    print("\nActual Rules:")
    for key, value in actual_rules.items():
        print(f"{key}: {value}")

    print("\nExpected Rules:")
    for key, value in expected_rules.items():
        print(f"{key}: {value}")

    matched = compare_joint_positions(actual_rules, expected_rules)

    if matched>MATCH_THRESHOLD:
        print("\nExercise performed correctly.")
    else:
            print("\nExercise performance did not match the description.")

# Example usage for the specific kettlebell exercise
TEST_PATH = "../test_json"
gpt_rules = {}
for filename in os.listdir(TEST_PATH):
    base_name = os.path.splitext(filename)[0]
    currpath = os.path.join(TEST_PATH,filename)
    with open(currpath,'r') as file:
        data = json.load(file)
        gpt_rules[base_name] = data
    file.close()
print(gpt_rules)
