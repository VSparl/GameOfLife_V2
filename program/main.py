"""Making a module docstring so my linter shuts up"""
import msvcrt
import random
import os
import sys
from time import sleep
from colorama import Back, Fore

BOARDS_PATH: str = os.path.join("..", "boards")  # Path to where the boards are stored
FAVOURITES_PATH: str = os.path.join("..", "favourites")  # Favourite boards


class FileInvalidError(Exception):
    """Custom error for .gol files that don't pass the validity check."""
    def __init__(
        self,
        message="File didn't pass the validity check. "
        "All characters must be printable and all lines must have the same length."):
        self.message = message
        super().__init__(self.message)


def handle_special_args() -> None:
    """Handle special args that start with a hyphen (-)

    Only one argument should be provided with the command in most cases,
    any others will be ignored.
    A list of special arguments is found below:

    -h to show help information and explain args.
    -l to list boards saved in the boards folder.
    -c to clear the entire boards folder (requires confirmation).
    -f to mark board after -f arg as favourite in special folder.
        Favourite files can only be deleted manually through
        e.g. the File Explorer.
    -n to override file specified after -n arg.
    """
    # TODO Make sure that the -h arg and the docstring say the same thing when done with implements
    if len(sys.argv) == 1:
        # No args to handle
        return
    arg1 = sys.argv[1]

    if arg1 == "-h":
        print("""
Usage: py main.py [arg]

The first argument is either ONLY a filename (with or without extension)
of a .gol board, or a special argument.
There will always only be ONE argument, except in the case of -f or -n

Special args can be the following:
-h to show this help message.
-l to list the saved boards using the board creator (standalone program or module).
-c to clear your boards folder.
-f to mark the board specified in the next argument as a favourite.
    Favourites can only be deleted manually in the file explorer.
-n to override the file specified after the -n argument""")
        sys.exit(0)

    if arg1 == "-l":
        print(f"Saved boards:\n{Fore.LIGHTBLUE_EX}")
        boards: list[str] = os.listdir(BOARDS_PATH)
        boards.sort()
        print("\n".join(boards))
        # Show absolute path of boards folder for easy access
        print(f"{Fore.RESET}\nYour boards are saved here: {os.path.abspath(BOARDS_PATH)}\n\n")

        print(f"Favourites:\n{Fore.LIGHTCYAN_EX}")
        boards: list[str] = os.listdir(FAVOURITES_PATH)
        boards.sort()
        print("\n".join(boards))
        # Show absolute path of boards folder for easy access
        print(f"{Fore.RESET}\nYour favourites are saved here: {os.path.abspath(BOARDS_PATH)}")

        sys.exit(0)

    if arg1 == "-c":
        if input("Are you sure you want to DELETE all of your saved boards?\n"
                 "Favourites will not be affected. [y/n] ").lower() == "y":
            for file in os.listdir(BOARDS_PATH):
                # Remove each file but leave the folder
                os.remove(os.path.join(BOARDS_PATH, file))

            print(f"{Fore.GREEN}SUCCESS: {Fore.RESET}Files deleted.")
        sys.exit(0)

    if arg1 == "-f" and len(sys.argv) > 2:
        fav_file = f"{sys.argv[2]}{".gol" if sys.argv[2][-4:] != ".gol" else ""}"

        if fav_file in os.listdir(BOARDS_PATH):
            # File is there, ready to move to favourites
            if input("Are you sure you want to move"
                     f" \"{fav_file}\" to favourites? [y/n] ").lower() == "y":
                os.makedirs(FAVOURITES_PATH, exist_ok=True)  # Create favourites directory
                # Move file, keeping the name
                os.rename(
                    os.path.join(BOARDS_PATH, fav_file),
                    os.path.join(FAVOURITES_PATH, fav_file))

                print(f"{Fore.GREEN}SUCCESS: {Fore.RESET}File moved successfully.")
                sys.exit(0)

        if fav_file in os.listdir(FAVOURITES_PATH):
            # File is already in favourites
            if input(f"\"{fav_file}\" is already in your favourites folder."
                     " Do you want to move it back to the other boards? [y/n] ").lower() == "y":
                os.makedirs(BOARDS_PATH, exist_ok=True)  # User might have deleted boards directory
                # Move file, keeping the name
                os.rename(
                    os.path.join(FAVOURITES_PATH, fav_file),
                    os.path.join(BOARDS_PATH, fav_file))

                print(f"{Fore.GREEN}SUCCESS: {Fore.RESET}File moved successfully.")
                sys.exit(0)

        print(f"{Fore.RED}ERROR: {Fore.RESET}File \"{fav_file}\" "
                "could not be found. No files were moved.")

        sys.exit(0)

    if arg1 == "-n" and len(sys.argv) > 2:
        # Set the name of the file to override
        file_to_override: str = f"{sys.argv[2]}{".gol" if sys.argv[2][-4:] != ".gol" else ""}"
        if input(f"""If the file doesn't exist yet, a new one will be created.
Are you sure you want to override the file \"{file_to_override}\"? [y/n] """).lower() == "y":
            print()
            manually_create_level(file_to_override)
        sys.exit(0)

    if arg1 == "-d" and len(sys.argv) > 2:
        # Set the name of the file to delete
        file_to_delete = f"{sys.argv[2]}{".gol" if sys.argv[2][-4:] != ".gol" else ""}"
        try:
            os.remove(os.path.join(BOARDS_PATH, file_to_delete))
        except FileNotFoundError:
            print(f"{Fore.RED}ERROR: {Fore.RESET}The filename \"{file_to_delete}\" "
                  "doesn't seem to exist, so nothing was deleted.")
        sys.exit(0)


def display_welcome() -> None:
    """Print some welcome words."""
    os.system("cls")
    print("Welcome to the Game of Life, blah blah blah...")


def get_start_board() -> list[list[bool]]:
    """Handle and return a board based on the command line arguments."""
    # Get filename to import from command line args
    filename: str = sys.argv[1] if len(sys.argv) > 1 else ""

    if filename:
        try:
            # Try to import the file from the specified filepath
            local_board = import_from_file(sys.argv[1])

        except TypeError:
            # File doesn't exist
            if input(f"{Fore.RED}ERROR:{Fore.RESET} Your file was not found.\n"
                     "Do you want to start the level editor to make your own board? [y/n] "
                     ).lower() == "y":
                # Prompt user to create their own board with the filename
                local_board = manually_create_level(filename)

            else: sys.exit(0)

        except FileInvalidError:
            print(f"{Fore.RED}ERROR: {Fore.RESET}File invalid. Try again with another file.")
            if input("Would you like to delete the file? [y/n] ").lower() == "y":
                # Delete invalid file
                if filename[-4:] != ".gol":
                    filename += ".gol"
                os.remove(os.path.join(BOARDS_PATH, filename))
                print(f"{Fore.GREEN}SUCCESS: {Fore.RESET}{filename} deleted successfully")

            sys.exit(1)

    else:
        local_board = generate_random_board()

    return local_board


def controlled_input(input_string: str, max_len: int) -> list[str]:
    """Input function but with max length

    Automatically returns and goes on to the next line when the specified
    input length has been reached.
    Still allows for Ctrl+C to interrupt the program.
    Special characters like ö, ñ etc. will be shown with a placeholder (�)
    as they are not UTF-8.
    This function was written with the help of ChatGPT.

    WARNING: This only works on Windows devices.
    """
    input_chars: list[str] = []
    print(input_string, end="", flush=True)

    while True:
        if msvcrt.kbhit():  # React to keyboard input
            # Get typed character from keyboard and decode it
            char = msvcrt.getch().decode("utf-8", "replace")
            # Handle all exceptions and special keys
            if char == "\x03":  # Ctrl+C
                # Simulate same behaviour of "regular" Ctrl+C
                raise KeyboardInterrupt

            if char == "\x08":  # Backspace key
                if input_chars:
                    input_chars.pop()
                    # Move cursor back, overwrite character with a space
                    print("\b \b", end="", flush=True)
                continue

            if char == "\r":  # Enter key
                # Function returns automatically
                continue

            # Add typed character to list and print it to the screen
            input_chars.append(char)
            print(char, end="", flush=True)

            if len(input_chars) >= max_len:
                # Desired length reached
                break

    print()
    return input_chars


def generate_random_board(height: int = -1, width: int = -1) -> list[list[bool]]:
    """Generates a random starting configuration of a board.

    Arguments specify the size of the board.
    A cell has a 50% chance to contain a counter.

    If the args are -1 for both height and width, the numbers will be
    selected so that the game consumes the entire screen.
    """
    local_board: list[list[bool]] = []

    if (height, width) == (-1, -1):
        # Fill the entire screen
        terminal = os.get_terminal_size()
        # Sometimes the size function returns one line too many
        height = terminal.lines - 1
        # One cell is 2 chars wide
        width = terminal.columns // 2

    for _ in range(height):
        processed_input = [(random.random() <= 0.5) for _ in range(width)]
        local_board.append(processed_input)

    return local_board


def import_from_file(filepath: str) -> list[list[bool]]:
    """Turns a file into a proper list and checks the validity of the board."""
    local_board: list[list[bool]] = []
    line: str = "PLACEHOLDER"

    # Add file extension if it wasn't provided
    if filepath[-4:] != ".gol":
        filepath += ".gol"

    target = BOARDS_PATH if filepath in os.listdir(BOARDS_PATH) else FAVOURITES_PATH if filepath in os.listdir(FAVOURITES_PATH) else None

    with open(os.path.join(target, filepath), "r", encoding="utf-8") as fp:
        print(f"{Fore.GREEN}SUCCESS: {Fore.RESET}File found, initializing...")
        sleep(1.2)

        while line:
            line = fp.readline().strip("\n")
            # Convert char to bool value
            processed_line = [not char == " " for char in line]
            if processed_line:
                # Avoids empty lists, they exist for some reason
                local_board.append(processed_line)

    if check_validity(local_board):
        return local_board

    # File is faulty
    raise FileInvalidError


def check_validity(board: list[list[bool]]) -> bool:
    """Check if the formatting is valid in a starting configuration file.

    Count the different lengths of rows on a board.
    All rows should be the same length.
    """
    last_col = -1
    diff_cols = 0
    for _, col in enumerate(board[:-1]):
        curr_col = len(col)

        if curr_col != last_col:
            diff_cols += 1

        last_col = curr_col

    return diff_cols == 1


def manually_create_level(filename: str="") -> list[list[bool]]:
    """Create a level according to user specifications.

    If no filename is specified, it will only return the board.
    The new level will be saved in a .gol file as characters
    if a filename is specified.
    """
    local_board: list[list[str]] = []

    print()
    # Get parameters for the board from the user
    while True:
        width: str = input("Enter board width (chars): ")
        if not width.isnumeric() or int(width) <= 1:
            print("Minimum value is 2. Please only write numbers\n")
            continue

        height: str = input("Enter board height (chars): ")
        if not height.isnumeric() or int(height) <= 1:
            print("Minimum value is 2. Please only write numbers\n")
            continue

        height, width = int(height), int(width)
        break

    # Set up file-related stuff
    if filename:  # Do only if config should be saved in a file
        # Add file extension if not present
        if filename[-4:] != ".gol":
            filename += ".gol"

        # If directory doesn't exist yet, create it
        os.makedirs(BOARDS_PATH, exist_ok=True)

        # Open file to save config in
        fp = open(os.path.join(BOARDS_PATH, filename), "w", encoding="utf-8")

    print()
    # Actually get and save input
    for i in range(height):
        # Format and write chars entered by user
        line: list[str] = controlled_input(f"Enter line No. {i + 1}: ", width)
        # Directly convert input to bool values
        processed_input = [not char == " " for char in line]
        local_board.append(processed_input)

        if filename:
            # Include in file if specified
            fp.write("".join(line))

            if i != height - 1:
                # Don't write last newline
                fp.write("\n")

    if filename: # Again, only if saved in file
        print(f"\n{Fore.GREEN}SUCCESS: {Fore.RESET}File created successfully!")

    fp.close()
    return local_board


def count_neighbors(board: list[list[bool]], row: int, col: int) -> int:
    """Count the number of live neighbors for a given cell.

    Iterate over relative positions of neighbour cells
    and check the state of the counters inside.
    """
    # Relative position of the cells neighbours
    neighbour_rel_pos: list = [(row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
                               (row, col - 1),                     (row, col + 1),
                               (row + 1, col - 1), (row + 1, col), (row + 1, col + 1),]

    live_neighbors: int = 0
    for i, j in neighbour_rel_pos:
        #           counter is in a valid position          cell is alive
        if (0 <= i < len(board) and 0 <= j < len(board[0])) and board[i][j]:
            live_neighbors += 1

    return live_neighbors


def update_board(board: list[list[bool]]) -> list[list[bool]]:
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


def print_board(local_board: list[list[bool]], character: str = " ") -> None:
    """Print the current state of the board.

    Colorama is used to draw colored characters.
    Live cells are displayed as green.
    The specified character is used to fill the cells, default is empty.
    """
    live_cells = 0

    os.system("cls")  # Clear the terminal

    for row in local_board:
        for cell in row:
            # Color only if cell is alive
            if cell:
                print(f"{Back.GREEN}{character} {Back.RESET}", end="")
                live_cells += 1
            else:
                print(f"{character} ", end="")
        print()  # New line after row

    if live_cells == 0:
        # Entire board is dead
        end_game()


def end_game() -> None:
    """Finish the game and display some text as the end"""
    print("Game finished.")
    # Exit program with code 0
    sys.exit(0)


if __name__ == "__main__":
    handle_special_args()
    display_welcome()
    global_board = get_start_board()

    # Avoid stuck screens that only include still lives
    last_board:list[list[bool]] = []

    # Main game loop
    while last_board != global_board:
        print_board(global_board)
        last_board = global_board
        global_board = update_board(global_board)
        sleep(0.25)
