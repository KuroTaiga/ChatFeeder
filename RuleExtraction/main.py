from exercise_analyzer import process_video_with_rules, compare_with_reference_exercises
from GYMDetector import YOLOv7EquipmentDetector, PoseDetector
from helper import get_video_path
from constants import EQUIPMENTS
from exercise_rules import build_exercise_rules_json, get_exercise_names
from exercise_reporter import ExerciseAnalysisReporter
import json
import os

def main():
    # Initialize paths and constants
    video_root_dir = "../blender_mp4/"
    model_path = "./assets/best-v2.pt"
    reference_json = "./results.json"
    output_dir = "./analysis_results"
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Initialize reporter
    reporter = ExerciseAnalysisReporter()

    # Load exercise rules and get exercise names
    exercises_rules = build_exercise_rules_json()
    exercises_names = get_exercise_names(exercises_rules)
    
    print(f"Looking for these exercises: {exercises_names}")

    # Initialize detectors
    equipment_detector = YOLOv7EquipmentDetector(model_path, EQUIPMENTS)
    pose_detector = PoseDetector()

    # Get video paths
    video_list, target_exercise_names = get_video_path(video_root_dir, exercises_names)
    
    if not video_list:
        print("No matching videos found!")
        return
        
    print(f"Found {len(video_list)} matching videos")

    # Process each video
    for video_path, activity_name in zip(video_list, target_exercise_names):
        print(f"\nProcessing video: {activity_name}")
        
        # Process video and extract rules
        extracted_rules = process_video_with_rules(
            video_path, 
            equipment_detector, 
            pose_detector
        )
        
        # Find matching exercises
        matches = compare_with_reference_exercises(
            extracted_rules,
            reference_json,
            top_n=3
        )
        
        # Add result to reporter
        reporter.add_result(activity_name, extracted_rules, matches)
        
        # Print immediate results
        print(f"\nResults for {activity_name}:")
        print("Top 3 Matching Exercises:")
        for exercise, score in matches:
            print(f"{exercise}: {score:.2f}")
        print("\n" + "="*50 + "\n")
    
    # Generate and save reports
    reporter.save_results(output_dir)
    
    # Print final summary
    print("\nFinal Summary:")
    print(reporter.generate_detailed_report())

if __name__ == "__main__":
    main()