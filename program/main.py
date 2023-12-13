"""Making a module docstring so my linter shuts up"""
import msvcrt
import random
from time import sleep
from colorama import Back


def display_welcome() -> None:
    """Print some welcome words."""
    print("Welcome to the Game of Life, blah blah blah...")


def end_game() -> None:
    """Finish the game and display some text as the end"""
    print("Game finished.")
    quit()


def controlled_input(input_string: str, max_len: int) -> list:
    """Input function but with max length

    Automatically returns and goes on to the next line when the specified
    input length has been reached.
    Still allows for Ctrl+C to interrupt the program.
    This function was written with the help of ChatGPT.

    WARNING: This only works on Windows devices.
    """
    input_chars: list[str] = []
    print(input_string, end='', flush=True)
    while True:
        if msvcrt.kbhit():  # React to keyboard input
            # Get typed character from keyboard and decode it
            char = msvcrt.getch().decode('utf-8')
            # Handle all exceptions and special keys
            if char == '\x03':  # Ctrl+C
                # Simulate same behaviour of "regular" Ctrl+C
                raise KeyboardInterrupt

            if char == '\x08':  # Backspace key
                if input_chars:
                    input_chars.pop()
                    # Move cursor back, overwrite character with a space
                    print('\b \b', end='', flush=True)
                continue

            if char == '\r':  # Enter key
                # Function returns automatically
                continue

            # Add typed character to list and print it to the screen
            input_chars.append(char)
            print(char, end='', flush=True)

            if len(input_chars) >= max_len:
                # Desired length reached
                break

    print()
    return input_chars


def get_starting_position(height: int, width: int) -> list[list[bool]]:
    """Get the initial board status from the user.

    Return the board as a nested list of rows containing
    boolean values indicating the state of the cell.
    """
    local_board: list[list[bool]] = []

    for i in range(height):
        usr_input: list[str] = controlled_input(f"Enter row No. {i + 1}: ", width)
        # Turn non-space characters into True vaules and spaces into False
        processed_input = [not char == ' ' for char in usr_input]
        local_board.append(processed_input)

    return local_board


def generate_random_board(height: int, width: int) -> list[list[bool]]:
    """Generates a random starting configuration of a board.

    Arguments specify the size of the board.
    A cell has a 33% chance to contain a counter.
    """
    local_board: list[list[bool]] = []

    for _ in range(height):
        processed_input = [random.choice([True, False, False]) for _ in range(width)]
        local_board.append(processed_input)

    return local_board


def count_neighbors(board, row, col):
    """Count the number of live neighbors for a given cell."""
    neighbors = [(row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
                 (row, col - 1),                     (row, col + 1),
                 (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)]

    live_neighbors = 0
    for i, j in neighbors:
        if 0 <= i < len(board) and 0 <= j < len(board[0]) and board[i][j]:
            live_neighbors += 1

    return live_neighbors

def update_board(board):
    """Update the board according to the rules of the Game of Life."""
    # Initialize a board where all cells are dead
    new_board: list[list[bool]] = [[False] * len(board[0]) for _ in range(len(board))]

    for i, _ in enumerate(board):
        for j, counter in enumerate(board[i]):
            live_neighbors = count_neighbors(board, i, j)

            # Apply Game of Life rules
            #     live cell has 2 or 3 neighbours           cell is a birth cell -> 3 neighbours
            if (counter and (live_neighbors in (2, 3))) or (not counter and live_neighbors == 3):
                new_board[i][j] = True

    return new_board


def print_board(local_board):
    """Print the current state of the board.

    Colorama is used to draw colored characters.
    Live cells are displayed as green."""
    live_cells = 0

    for row in local_board:
        for cell in row:
            # Color only if cell is alive
            if cell:
                print(f"{Back.GREEN}▯ {Back.RESET}", end='')
                live_cells += 1
            else:
                print("▯ ", end='')
        print()  # New line after row

    if live_cells == 0:
        end_game()


if __name__ == "__main__":
    display_welcome()
    global_board = generate_random_board(5, 5)
    last_board = []

    while last_board != global_board:
        print_board(global_board)
        print("\n" + "-" * 20 + "\n")
        last_board = global_board
        global_board = update_board(global_board)
        sleep(0.2)
        input()

    print_board(global_board)
    print("\n" + "-" * 20 + "\n")
    last_board = global_board
    global_board = update_board(global_board)
    sleep(0.2)
