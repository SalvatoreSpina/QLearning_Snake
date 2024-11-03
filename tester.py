import subprocess
import os
import argparse

# Define the model directory
model_directory = 'models'

session_counts = [1, 10, 100, 1000, 10000]

# Ensure the models directory exists
if not os.path.exists(model_directory):
    raise FileNotFoundError(f"The directory {model_directory} does not exist.")

# Parse the argument
parser = argparse.ArgumentParser(description='Run tests on models.')
parser.add_argument('test_type', type=str, help='Type of test to run (e.g., test_model)')
args = parser.parse_args()

# Check the type of test
if args.test_type == 'test_model':
    for session_count in session_counts:
        # Construct the model file name based on the session count
        model_file = f'model_{session_count}.txt'
        model_path = os.path.join(model_directory, model_file)
        
        # Check if the model file exists
        if not os.path.exists(model_path):
            print(f"The model file {model_path} does not exist. Skipping...")
            continue
        
        # Construct the command
        command = [
            'python3', 'main.py',
            '-sessions', '100',
            '-load', model_path,
            '-visual', 'off',
            '-learn', 'off',
            '-print', 'off'
        ]
        
        # Run the command
        print(f"Executing: {' '.join(command)}")
        subprocess.run(command)
        print("--------------------")
elif args.test_type == 'best_model':
    
    model_file = f'model_{1000000}.txt'
    model_path = os.path.join(model_directory, model_file)
    command = [
        'python3', 'main.py',
        '-sessions', '5',
        '-load', model_path,
        '-visual', 'on',
        '-learn', 'off',
        '-print', 'off'
    ]
    
    print(f"Executing: {' '.join(command)}")
    subprocess.run(command)

elif args.test_type == 'superbonus' or args.test_type == 'visualize_superbonus':
    model_file = f'model_{1000000}.txt'
    model_path = os.path.join(model_directory, model_file)
    
    sessionss_count = 1000 if args.test_type == 'superbonus' else 10
    visual = 'on' if args.test_type == 'visualize_superbonus' else 'off'
    
    command = [
        'python3', 'main.py',
        '-sessions', str(sessionss_count),
        '-board', '20',
        '-load', model_path,
        '-visual', visual,
        '-learn', 'off',
        '-print', 'off'
    ]
    
    print(f"Executing: {' '.join(command)}")
    subprocess.run(command)
    
else:
    print(f"Unknown test type: {args.test_type}")