
# Conway's Game of Life

## Overview
The Game of Life is a cellular automaton devised by mathematician John Conway in 1970. It's a zero-player game, meaning its evolution is determined by its initial state, with no further input. The game is played on a grid of cells, each of which can be in one of two states: alive or dead.

## Rules
1. **Birth**: A dead cell with *exactly three* live neighbors becomes alive in the next generation.
2. **Survival**: A live cell with *two or three* live neighbors survives to the next generation.
3. **Death**: A live cell with *fewer than two* live neighbors dies due to underpopulation, and a live cell with *more than three* live neighbors dies due to overpopulation.

## Usage
1. **Installation**: Clone the GitHub repository onto your machine. To do this, navigate to your directory of choice in your terminal and enter `git clone https://github.com/VSparl/GameOfLife_V2.git`

2. **Starting the Game**: Navigate into the `program` folder using `cd GameOfLife_V2/program`. Launch the game using the terminal command `py main.py` and add any additional arguments (maybe start with `-h` for some help).

3. **Initial State**: Depending on the argument(s) you selected (if any), you will either be prompted to create your own board or the game will make a randomized full-screen board for you and directly start the game.

4. **Running the Simulation**: If prompted, press `Enter` to start the simulation. The game will evolve through generations based on the rules stated above. Once the whole board either dies out (no more live cells) or the board only consists of  [still lives](https://en.wikipedia.org/wiki/Still_life_%28cellular_automaton%29), the game will stop automatically to avoid re-simulating the same scenario over and over again.

5. **Exiting**: To exit the game, press `Ctrl + C` to interrupt the program or follow on-screen instructions.

## History
Conway's Game of Life became widely known after Martin Gardner featured it in his column in Scientific American in October 1970. The game's simplicity and the emergence of complex patterns have made it a popular subject of study in computer science, mathematics, and various scientific fields.

## Educational significance
Beyond its scientific contributions, the Game of Life has become a popular educational tool. It is often used to introduce students to various concepts in computer science or mathematics. The simplicity of the rules and the visually compelling evolving patterns make it an interesting and interactive way to teach fundamental principles in a variety of applications. Many computer science courses incorporate the Game of Life to illustrate concepts such as cellular automata, algorithmic thinking, and causality when setting up systems of rules.
