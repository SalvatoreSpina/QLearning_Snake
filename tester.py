import subprocess
import os
import argparse

# Define the model directory
model_directory = 'models'

# Ensure the models directory exists
if not os.path.exists(model_directory):
    raise FileNotFoundError(f"The directory {model_directory} does not exist.")

# Parse the argument
parser = argparse.ArgumentParser(description='Run tests on models.')
parser.add_argument('test_type', type=str, help='Type of test to run (e.g., test_model)')
args = parser.parse_args()

# Check the type of test
if args.test_type == 'test_model':
    # List all model files in the directory
    model_files = [f for f in os.listdir(model_directory) if f.endswith('.txt')]
    
    # Iterate over the model files and run the command
    print(f"Testing {len(model_files)} models...")
    for model_file in model_files:
        model_path = os.path.join(model_directory, model_file)
        # Construct the command
        command = [
            'python3', 'main.py',
            '-sessions', '100',
            '-learn', 'off',
            '-visual', 'off',
            '-print', 'off',
            '-load', model_path,
        ]
        # Run the command
        print(f"Command: {' '.join(command)}")
        subprocess.run(command)
else:
    print(f"Unknown test type: {args.test_type}")