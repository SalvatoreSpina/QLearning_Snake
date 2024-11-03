import subprocess
import os

# Define the session counts and corresponding model filenames
session_counts = [1, 10, 100, 1000, 10000, 100000]
model_directory = 'models'  # Ensure this directory exists or create it

# Ensure the models directory exists
if not os.path.exists(model_directory):
    os.makedirs(model_directory)

# Iterate over the session counts and generate models
for sessions in session_counts:
    model_filename = f"{model_directory}/model_{sessions}.txt"
    # Construct the command
    command = [
        'python3', 'main.py',
        '-sessions', str(sessions),
        '-save', model_filename,
        '-visual', 'off',
        '-learn', 'on',
        '-print', 'off',
    ]
    print(f"Executing: {' '.join(command)}")
    # Run the command
    subprocess.run(command)
    print("--------------------")