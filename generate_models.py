import os
import subprocess


# Define the session counts and corresponding model filenames
SESSION_COUNTS = [1, 10, 100, 1000, 10000, 100000]
MODEL_DIRECTORY = 'models'  # Ensure this directory exists or create it

# Ensure the models directory exists
os.makedirs(MODEL_DIRECTORY, exist_ok=True)


def generate_model(sessions):
    """Generate a model for a given number of sessions."""
    model_filename = f"{MODEL_DIRECTORY}/model_{sessions}.txt"
    command = [
        'python3', 'main.py',
        '-sessions', str(sessions),
        '-save', model_filename,
        '-visual', 'off',
        '-learn', 'on',
        '-print', 'off',
    ]
    print(f"Executing: {' '.join(command)}")
    subprocess.run(command)
    print("--------------------")


def main():
    """Main function to generate models for all session counts."""
    for sessions in SESSION_COUNTS:
        generate_model(sessions)


if __name__ == "__main__":
    main()
