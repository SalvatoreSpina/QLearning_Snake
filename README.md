# 🐍 Snake Q-Learning Agent

![Snake Game](https://user-images.githubusercontent.com/yourusername/yourrepository/snake-game-screenshot.png)

## 📝 Table of Contents

- [🧐 Description](#-description)
- [🚀 Features](#-features)
- [🛠 Technologies Used](#-technologies-used)
- [🔧 Installation](#-installation)
- [🎮 Usage](#-usage)
- [📄 License](#-license)

## 🧐 Description

**Snake Q-Learning Agent** is a Python-based implementation of the classic Snake game enhanced with a Q-Learning AI agent. This project demonstrates how reinforcement learning can be applied to game development, allowing the snake to learn and improve its performance over time. Whether you're interested in game development, artificial intelligence, or both, this project offers valuable insights and a hands-on experience.

## 🚀 Features

- **Reinforcement Learning:** Implements a Q-Learning agent that learns optimal strategies to maximize the snake's survival and growth.
- **Visualization:** Interactive game interface using Pygame to visualize the snake's movements and decisions.
- **Model Persistence:** Save and load trained models to continue training or deploy the agent.
- **Customizable Parameters:** Adjust game settings such as board size, speed, visualization, and learning preferences via command-line arguments.
- **Step-by-Step Execution:** Observe the agent's decision-making process in real-time.
- **Terminal Feedback:** Real-time statistics and state information printed in the terminal for deeper insights.
- **Robust Error Handling:** Ensures smooth execution and model management.

## 🛠 Technologies Used

- **Programming Language:** Python 3.x
- **Libraries & Frameworks:**
  - [Pygame](https://www.pygame.org/news) for game development and visualization.
  - [NumPy](https://numpy.org/) for numerical computations.
  - [Argparse](https://docs.python.org/3/library/argparse.html) for parsing command-line arguments.
  - [JSON](https://docs.python.org/3/library/json.html) for model serialization.
- **Others:**
  - Git for version control.

## 🔧 Installation

Follow these steps to set up the project locally:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/snake-q-learning-agent.git
   cd snake-q-learning-agent
   ```

2. **Create a Virtual Environment (Optional but Recommended)**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   *If a `requirements.txt` is not provided, install the necessary packages manually:*

   ```bash
   pip install pygame numpy
   ```

## 🎮 Usage

Run the game with default settings:

```bash
python main.py
```

### **Command-Line Arguments**

Customize the game's behavior using the following arguments:

- `-sessions`: **Number of training sessions**
  - **Type:** Integer
  - **Default:** `1`
  - **Example:** `-sessions 1000`

- `-save`: **File to save the trained model**
  - **Type:** String (Filename)
  - **Default:** `''` (No saving)
  - **Example:** `-save models/snake_model.json`

- `-load`: **File to load a pre-trained model**
  - **Type:** String (Filename)
  - **Default:** `''` (No loading)
  - **Example:** `-load models/snake_model.json`

- `-visual`: **Toggle visualization**
  - **Choices:** `on`, `off`
  - **Default:** `on`
  - **Example:** `-visual off`

- `-learn`: **Enable or disable learning**
  - **Choices:** `on`, `off`
  - **Default:** `on`
  - **Example:** `-learn off`

- `-board_size`: **Size of the game board**
  - **Type:** Integer
  - **Default:** `20` (Assuming `BOARD_SIZE = 20` in `config.py`)
  - **Example:** `-board_size 30`

- `-speed`: **Game speed**
  - **Choices:** `Really Slow`, `Slow`, `Normal`, `Fast`
  - **Default:** `Normal`
  - **Example:** `-speed Fast`

- `-print`: **Enable or disable terminal printing**
  - **Choices:** `on`, `off`
  - **Default:** `on`
  - **Example:** `-print off`

- `-step_by_step`: **Enable or disable step-by-step execution**
  - **Choices:** `on`, `off`
  - **Default:** `off`
  - **Example:** `-step_by_step on`

### **Example Usage**

1. **Train the Agent for 1000 Sessions and Save the Model**

   ```bash
   python main.py -sessions 1000 -save models/snake_model.json
   ```

2. **Run the Game Without Visualization and Disable Learning**

   ```bash
   python main.py -visual off -learn off
   ```

3. **Load a Pre-Trained Model and Observe in Step-by-Step Mode**

   ```bash
   python main.py -load models/snake_model.json -step_by_step on
   ```

## 📄 License

This project is licensed under the [MIT License](LICENSE).  
*Feel free to choose another license if it better suits your needs.*
