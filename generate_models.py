import subprocess
import os

# Define the session counts and corresponding model filenames
session_counts = [1, 10, 100, 1000, 100000]
model_directory = 'models'  # Ensure this directory exists or create it

# Ensure the models directory exists
if not os.path.exists(model_directory):
    os.makedirs(model_directory)

# Iterate over the session counts and generate models
for sessions in session_counts:
    model_filename = f"{model_directory}/{sessions}sess.txt"
    stats_filename = f"{model_directory}/{sessions}sess_stats.txt"
    print(f"Generating model with {sessions} sessions...")
    # Construct the command
    command = [
        'python', 'main.py',
        '-sessions', str(sessions),
        '-save', model_filename,
        '-visual', 'off',
        '-learn', 'on',
        '-print', 'off',
        '-stats_file', stats_filename
    ]
    # Run the command
    subprocess.run(command)
    # Read the stats from the stats file
    if os.path.exists(stats_filename):
        with open(stats_filename, 'r') as f:
            stats = f.read()
        print(f"Model saved to {model_filename}")
        print(f"Training Stats:\n{stats}\n")
    else:
        print(f"Stats file not found for model with {sessions} sessions.\n")
