# Q-Learning Snake

A simple reinforcement learning project where a snake learns to survive using the Q-learning algorithm. The game can run with or without a graphical interface powered by **pygame**.

![Menu](https://github.com/SalvatoreSpina/QLearning_Snake/blob/main/assets/menu.png)
![Game](https://github.com/SalvatoreSpina/QLearning_Snake/blob/main/assets/game.png)

## Features

- Q-learning agent with adjustable hyperparameters
- Save and load training models
- Optional visualization and step-by-step mode
- Fully configurable board size, speed and number of sessions

## Project layout

```
qlearning_snake/   Python package containing the game logic
assets/            Images used by the GUI
models/            Saved Q-table files
main.py            Entry point
generate_models.py Example helper script to train multiple models
tester.py          Utility for running automated tests on models
```

## Installation

Install the required packages with pip:

```bash
pip install -r requirements.txt
```

## Usage

Run the game with default options:

```bash
python main.py
```

Useful command line arguments:

- `-sessions` number of training sessions (default: 1)
- `-save` file path to store the trained model
- `-load` file path of a previously saved model
- `-visual` `on` or `off` to enable graphics
- `-learn` `on` or `off` to disable learning
- `-board_size` size of the square board
- `-speed` one of `Really Slow`, `Slow`, `Normal`, `Fast`
- `-print` `on` or `off` to print states to terminal
- `-step_by_step` `on` or `off` to pause after each step

Example training run:

```bash
python main.py -sessions 1000 -save models/snake.json -visual off
```

## License

This project is released under the [MIT License](LICENSE).
