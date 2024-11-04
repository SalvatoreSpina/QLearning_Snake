import os
import argparse
import subprocess

# Define the model directory
MODEL_DIRECTORY = 'models'
BEST_MODEL = 'model_100000.txt'
SESSION_COUNTS = [1, 10, 100, 1000, 10000, 100000]

# Ensure the models directory exists
if not os.path.exists(MODEL_DIRECTORY):
    raise FileNotFoundError(f"The directory {MODEL_DIRECTORY} does not exist.")

# Parse the argument
parser = argparse.ArgumentParser(description='Run tests on models.')
parser.add_argument('test_type', type=str,
                    help='Type of test to run (e.g., test_model)')
args = parser.parse_args()


def run_command(command):
    """Run the given command using subprocess."""
    print(f"Executing: {' '.join(command)}")
    subprocess.run(command)
    print("--------------------")


def test_model():
    """Run tests on different models based on session counts."""
    for session_count in SESSION_COUNTS:
        model_file = f'model_{session_count}.txt'
        model_path = os.path.join(MODEL_DIRECTORY, model_file)

        if not os.path.exists(model_path):
            print(f"The model file {model_path} does not exist. Skipping...")
            continue

        command = [
            'python3', 'main.py',
            '-sessions', '100',
            '-load', model_path,
            '-visual', 'off',
            '-learn', 'off',
            '-print', 'off'
        ]
        run_command(command)


def best_model():
    """Run test on the best model."""
    model_path = os.path.join(MODEL_DIRECTORY, BEST_MODEL)
    command = [
        'python3', 'main.py',
        '-sessions', '5',
        '-load', model_path,
        '-visual', 'on',
        '-learn', 'off',
        '-print', 'off'
    ]
    run_command(command)


def superbonus(test_type):
    """Run superbonus or visualize_superbonus test."""
    model_path = os.path.join(MODEL_DIRECTORY, BEST_MODEL)
    sessions_count = 1000 if test_type == 'superbonus' else 10
    visual = 'on' if test_type == 'visualize_superbonus' else 'off'

    command = [
        'python3', 'main.py',
        '-sessions', str(sessions_count),
        '-board', '15',
        '-load', model_path,
        '-visual', visual,
        '-learn', 'off',
        '-print', 'off'
    ]
    run_command(command)


# Check the type of test
if args.test_type == 'test_model':
    test_model()
elif args.test_type == 'best_model':
    best_model()
elif args.test_type in ['superbonus', 'visualize_superbonus']:
    superbonus(args.test_type)
else:
    print(f"Unknown test type: {args.test_type}")
