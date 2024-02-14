# Conway's Game of Life

## Overview
The Game of Life is a cellular automaton devised by mathematician John Conway in 1970. It's a zero-player game, meaning its evolution is determined by its initial state, with no further input. The game is played on a grid of cells, each of which can be in one of two states: alive or dead. Each generation is created by applying the game rules simultaneously to every cell on the board, so that births and deaths occur simultaneously.

## Rules
1.  **Birth**: A dead cell with *exactly three* live neighbors becomes alive in the next generation.

2.  **Survival**: A live cell with *two or three* live neighbors survives to the next generation.

3.  **Death**: A live cell with *fewer than two* live neighbors dies due to underpopulation, and a live cell with *more than three* live neighbors dies due to overpopulation.

## Usage
1.  **Installation**:

	If provided, use the `setup.py` module to automatically install and set up the game.

	If you don't have a `setup.py` script, install it manually instead:	
	Clone the GitHub repository onto your machine. To do this, navigate to your directory of choice in your terminal and enter `git clone https://github.com/VSparl/GameOfLife_V2.git`. Next, you will need to install the `colorama` module using `pip install colorama`.

3.  **Starting the Game**: Navigate into the `program` folder using `cd GameOfLife_V2/program`. Launch the game using the terminal command `py main.py` and add any additional arguments (maybe start with `-h` for some help).

4.  **Initial State**: Depending on the argument(s) you selected (if any), you will either be prompted to create your own board or the game will make a randomized full-screen board for you and directly start the game.

5.  **Running the Simulation**: If prompted, press `Enter` to start the simulation. The game will evolve through generations based on the rules stated above. Once the whole board either dies out (no more live cells) or the board only consists of [still lives](https://en.wikipedia.org/wiki/Still_life_%28cellular_automaton%29), the game will stop automatically to avoid re-simulating the same scenario over and over again. Any oscillating structures will continue to be simulated, even if they repeat themselves.

6.  **Exiting**: During a running simulation, press `Enter` to finish the simulation. Else, follow on-screen instructions or press `Ctrl + C` at any time to forcefully end the program (not recommended).

## Example boards
There are some example boards included with the repository to help the user get an idea of some of the different structures in the Game of Life. There are 3 differend pre-made structures available by default:
 - **101** is a structure that repeats itself forever, forming patterns that resemble zeros and ones changing. Open this board using `py main.py 101` or `py main.py 101.gol`.
 - A **Glider** is a small structure "gliding" accross the screen, hence their name. It doesn't change direction, but it will fly forever. To see the glider flying until it hits the wall, run `py main.py glider` or `py main.py glider.gol`.
 - **Gosper glider gun** is a structure that creates gliders while keeping itself intact. 
 - **Fishing hook** is a structure that "eats" gliders that collide with it. In the example files, a fishing hook is placed at the bottom of the glider gun file. To see the glider gun and the fishing hook in action, run `py main.py glider_gun` or `py main.py glider_gun.gol`.

## History
Conway's Game of Life is a cellular automaton devised by the British mathematician John Horton Conway in 1970. The game is a zero-player game, meaning that its evolution is determined by its initial state, requiring no further input. The game made its first public appearance in the October 1970 issue of Scientific American, in Martin Gardner's "Mathematical Games" column. The game's fundamental simplicity and the emergence of complex patterns - despite those straightforward laws - have made it a popular subject of study in computer science, mathematics, and various other scientific fields.

This simple set-up, played out by the computer over many generations creates vast complexity that is hard to watch without thinking of simple cellular organisms and their development. In fact, in 2010, a structure was created within the game by Andrew Wade [capable of reproducing itself](https://www.newscientist.com/article/mg20627653-800-first-replicating-creature-spawned-in-life-simulator/), reminding us of the real-life molecules that eventually lead to all the living creatures on earth.

## Educational significance
Beyond its scientific contributions, the Game of Life has become a popular educational tool. It is often used to introduce students to various concepts in computer science or mathematics. The simplicity of the rules and the visually compelling evolving patterns make it an interesting and interactive way to teach fundamental principles in a variety of applications. Many computer science courses incorporate the Game of Life to illustrate various concepts such as cellular automata, algorithmic thinking, and causality when setting up systems of rules.

## One-liner program
There also is a one-line version of the `main.py` program included in the repository. This is not meant to be a serious version of the program as the `exec()` function in python is inefficient and the code is not elegant at all. The reason for the creation of the one-line version was me being bored during an informatics lesson. I wrote a program to read through the original `main.py` file and replace quotes, newline characters, backslashes etc. to create a viable one-line python string to be executed. This is not meant to replace the proper `main.py` program and is not meant to be included in the grading of the project.