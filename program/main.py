"""Making a module docstring so my linter shuts up"""
import msvcrt
from colorama import Back


def display_welcome() -> None:
    """Print some welcome words."""
    print("Welcome to the Game of Life, blah blah blah...")


def controlled_input(input_string: str, max_len: int) -> list:
    """Input function but with max length

    Automatically returns and goes on to the next line when the specified
    input length has been reached.
    Still allows for Ctrl+C to interrupt the program.
    This function was written with the help of ChatGPT.

    WARNING: This only works on Windows devices.
    """
    input_chars: list = []
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


def get_starting_position(rows: int, cols: int) -> list[list[bool]]:
    """Get the initial board status from the user.

    Return the board as a nested list of rows containing
    boolean values indicating the state of the cell.
    """
    local_board: list[list[bool]] = []

    for i in range(rows):
        usr_input: str = controlled_input(f"enter row No. {i + 1}: ", cols)
        # Turn non-space characters into True vaules and spaces into False
        processed_input = [not char == ' ' for char in usr_input]
        local_board.append(processed_input)

    return local_board


def print_board(local_board):
    """Print the current state of the board.

    Colorama is used to draw colored characters.
    Live cells are displayed as green."""
    for row in local_board:
        for cell in row:
            # Color only if cell is alive
            print(f"{Back.GREEN}  {Back.RESET}" if cell else "  ", end='')
        print()  # New line


def main():
    """Docstring so the linter shuts up."""
    display_welcome()
    global_board = get_starting_position(30, 20)
    print_board(global_board)


main()
