import os
import json
import pandas as pd
from deepdiff import DeepDiff  # This library will help identify differences between two dictionaries

# Load results.json
with open('./results.json') as results_file:
    results_data = json.load(results_file)

# Prepare a list to store rows for the Excel file
rows = []

# Directory containing other JSON files
json_folder = '../test_json/'  # Replace with your folder path

# Loop through each exercise in results.json
for exercise in results_data['exercises']:
    activity_name = exercise['activity'].lower()
    

    result_rules = exercise['body_landmarks']  # Rules from results.json

    # Search for a corresponding file in the JSON folder
    for json_file_name in os.listdir(json_folder):
        if json_file_name.endswith('.json'):
            with open(os.path.join(json_folder, json_file_name)) as json_file:
                json_data = json.load(json_file)
                print(json_data.get('activity').lower())
                # Check if the activity matches
                if json_data.get('activity').lower() == activity_name:
                    file_rules = json_data['body_landmarks']  # Rules from other JSON file

                    # Compare the result rules and file rules using DeepDiff to highlight differences
                    differences = DeepDiff(result_rules, file_rules, ignore_order=True).to_json()

                    # Append data to the rows list
                    rows.append({
                        'Activity': activity_name,
                        'Result Rules': json.dumps(result_rules),
                        'File Rules': json.dumps(file_rules),
                        'Differences': differences if differences != '{}' else 'No differences'
                    })
                    break  # Stop searching further once the activity is found

# Convert the rows to a pandas DataFrame
df = pd.DataFrame(rows)

# Save to Excel file
output_path = './exercise_comparison_with_differences.xlsx'
df.to_excel(output_path, index=False)

print(f'Excel file generated at {output_path}')
