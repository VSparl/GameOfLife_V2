  

# Conway's Game of Life

  

## Overview

The Game of Life is a cellular automaton devised by mathematician John Conway in 1970. It's a zero-player game, meaning its evolution is determined by its initial state, with no further input. The game is played on a grid of cells, each of which can be in one of two states: alive or dead. Each generation is created by applying the game rules simultaneously to every cell on the board, births and deaths occur simultaneously.

  

## Rules

1.  **Birth**: A dead cell with *exactly three* live neighbors becomes alive in the next generation.

2.  **Survival**: A live cell with *two or three* live neighbors survives to the next generation.

3.  **Death**: A live cell with *fewer than two* live neighbors dies due to underpopulation, and a live cell with *more than three* live neighbors dies due to overpopulation.

  

## Usage

1.  **Installation**: 
	1. If provided, use the `setup.py` module to automatically install and set up the game.
	2. If you don't have a `setup.py` script, install it manually instead:

		Clone the GitHub repository onto your machine. To do this, navigate to your directory of choice in your terminal and enter `git clone https://github.com/VSparl/GameOfLife_V2.git`. Next, you will need to install the `colorama` module using `pip install colorama`.

  

2.  **Starting the Game**: Navigate into the `program` folder using `cd GameOfLife_V2/program`. Launch the game using the terminal command `py main.py` and add any additional arguments (maybe start with `-h` for some help).

  

3.  **Initial State**: Depending on the argument(s) you selected (if any), you will either be prompted to create your own board or the game will make a randomized full-screen board for you and directly start the game.

  

4.  **Running the Simulation**: If prompted, press `Enter` to start the simulation. The game will evolve through generations based on the rules stated above. Once the whole board either dies out (no more live cells) or the board only consists of [still lives](https://en.wikipedia.org/wiki/Still_life_%28cellular_automaton%29), the game will stop automatically to avoid re-simulating the same scenario over and over again. Any oscillating structures will continue to be simulated, even if they repeat themselves.

  

5. **Exiting**: During a running simulation, press `Enter` to finish the simulation. Else, follow on-screen instructions or press `Ctrl + C` at any time to forcefully end the program (not recommended).

  

## History

Conway's Game of Life is a cellular automaton devised by the British mathematician John Horton Conway in 1970. The game is a zero-player game, meaning that its evolution is determined by its initial state, requiring no further input. The game made its first public appearance in the October 1970 issue of Scientific American, in Martin Gardner's "Mathematical Games" column. The game's fundamental simplicity and the emergence of complex patterns - despite those straightforward laws - have made it a popular subject of study in computer science, mathematics, and various other scientific fields.

  

This simple set-up, played out by the computer over many generations creates vast complexity that is hard to watch without thinking of simple cellular organisms and their development. In fact, in 2010, a structure was created within the game by Andrew Wade [capable of reproducing itself](https://www.newscientist.com/article/mg20627653-800-first-replicating-creature-spawned-in-life-simulator/), reminding us of the real-life molecules that eventually lead to all the living creatures on earth.

  

## Educational significance

Beyond its scientific contributions, the Game of Life has become a popular educational tool. It is often used to introduce students to various concepts in computer science or mathematics. The simplicity of the rules and the visually compelling evolving patterns make it an interesting and interactive way to teach fundamental principles in a variety of applications. Many computer science courses incorporate the Game of Life to illustrate various concepts such as cellular automata, algorithmic thinking, and causality when setting up systems of rules.
