# main.py

from Game import GameUI
import argparse
from config import BOARD_SIZE

def main():
    parser = argparse.ArgumentParser(description='Snake Q-Learning Agent')
    parser.add_argument('-sessions', type=int, default=1, help='Number of training sessions')
    parser.add_argument('-save', type=str, default='', help='File to save the model')
    parser.add_argument('-load', type=str, default='', help='File to load the model')
    parser.add_argument('-visual', type=str, choices=['on', 'off'], default='on', help='Turn visualization on or off')
    parser.add_argument('-learn', type=str, choices=['on', 'off'], default='on', help='Enable or disable learning')
    parser.add_argument('-board_size', type=int, default=BOARD_SIZE, help='Size of the game board')
    parser.add_argument('-speed', type=str, choices=['Slow', 'Normal', 'Fast'], default='Normal', help='Game speed')
    parser.add_argument('-print', type=str, choices=['on', 'off'], default='on', help='Enable or disable terminal printing')
    parser.add_argument('-step_by_step', type=str, choices=['on', 'off'], default='off', help='Enable or disable step-by-step execution')

    args = parser.parse_args()

    # Initialize UI with command-line arguments as defaults
    ui = GameUI(
        board_size=args.board_size,
        sessions=args.sessions,
        save_file=args.save,
        load_file=args.load,
        visual=args.visual == 'on',
        learn=args.learn == 'on',
        speed=args.speed,
        print_terminal=args.print == 'on',
        step_by_step=args.step_by_step == 'on'
    )
    stats = ui.run()
    return stats

if __name__ == "__main__":
    stats = main()
    if stats:
        print(f"Max Length: {stats['max_length']}, Max Duration: {stats['max_duration']}")