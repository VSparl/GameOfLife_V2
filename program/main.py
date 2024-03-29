"""Python terminal implementation of John Conway's Game of Life."""
import sys
import os
import random
from time import sleep
try:
    # msvcrt is Windows-only
    import msvcrt
    MSVCRT_ERR = False
except ImportError:
    # Set error flag to true to avoid not running the program at all
    MSVCRT_ERR = True

try:
    # colorama needs to be installed separately
    from colorama import Back, Fore
except ImportError:
    print("Error importing modules. Please run setup.py from a windows environment."
          "Also chceck if your Python version supports the msvcrt module.\n")
    sys.exit(1)


class FileInvalidError(Exception):
    """Custom error for .gol files that don't pass the validity check."""
    def __init__(
        self,
        message="File didn't pass the validity check. "
        "All characters must be printable and all lines must have the same length."):
        self.message = message
        super().__init__(self.message)


def set_dir_and_os() -> None:
    """Set the starting directory and check that the program is run on Windows.

    Latter is due to the fact that the program can only run on windows.
    """
    # Set working directory to the program directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))


def clear() -> None:
    """Dynamic clear function, OS-dependent"""
    os.system("cls" if os.name == "nt" else "clear")


def check_origin(filename: str) -> str:
    """Check boards and favourites folder.

    Return the location of the file, or None if it doesn't exist.
    """
    return BOARDS_PATH if filename in os.listdir(BOARDS_PATH) \
    else FAVOURITES_PATH if filename in os.listdir(FAVOURITES_PATH) \
    else None


def handle_special_args() -> str:
    """Handle special args that start with a hyphen (-)

    Return the background character for the board or exit the program directly.

    Other arguments will only be taken into account if the
    first argument is valid.
    A list of special arguments is found below:

    -h to show a help message explaining the args and usage
    -l to list the saved boards using the board creator (standalone program or module).
    -e to erase all the files in the boards folder.
    -f to mark the board specified in the next argument as a favourite.
        Favourites are not affected by the -e argument.
        If the file is already in the favourites folder, offer to move it back.
    -n to create a new file with the specified name, even if a file with that name
        already exists.
    -d to delete the file, even if it is in the favourites folder.
    -c to select the character used for the board background.
        The -c arg is placed after the filename of a .gol board, if specified.
    -t to select the time to sleep inbetween printing boards. Default is 0.25 s.
    """
    # Setup default values for -c and -t args
    board_filler, timeout = " ", 0.25
    if len(sys.argv) == 1:
        # No args to handle, return default values
        return board_filler, timeout
    arg1 = sys.argv[1]
    finish = False

    if arg1 == "-h":  # Help
        print("""
Usage: py main.py [args]

The first argument is either ONLY a filename (with or without extension)
of a .gol board, or a special argument.
A second argument will only be taken into account if paired with a valid special argument.

Special args can be the following:
-h to show this help message.
-l to list the saved boards using the board creator (standalone program or module).
-e to erase your boards folder.
-f [filename] to mark the board specified as a favourite.
    Favourites are not affected by the -e argument.
    Also use this argument to move a board back from the favourites folder.
-n [filename] to create a new file with the specified name, even if a file with that name
    already exists.
-d [filename] to delete the file, even if it is in your favourites folder.
-c to select the character that fills the board as background.
    The -c argument is to be placed AFTER the name of a .gol board, if specified.
-t to select the amount of seconds between two generations. Default is 0.25 seconds.
    Keep in mind that the actual
    speed of generations still depends on the performance of your computer, especially
    for big boards.""")
        sys.exit(0)

    if arg1 == "-l":  # List
        boards: list[str] = os.listdir(BOARDS_PATH)
        boards.sort()

        print(f"Saved boards:\n{Fore.LIGHTBLUE_EX}")
        print("\n".join(boards) if len(boards) > 0 else "[Empty]")
        # Show absolute path of boards folder for easy access
        print(f"{Fore.RESET}\n{Fore.LIGHTBLACK_EX}"
              f"Your boards are saved here: {BOARDS_PATH}"
              f"{Fore.RESET}\n\n")

        boards: list[str] = os.listdir(FAVOURITES_PATH)
        boards.sort()

        print(f"Favourites:\n{Fore.LIGHTCYAN_EX}")
        print("\n".join(boards) if len(boards) > 0 else "[Empty]")
        # Show absolute path of boards folder for easy access
        print(f"{Fore.RESET}\n{Fore.LIGHTBLACK_EX}"
              f"Your favourites are saved here: {FAVOURITES_PATH}"
              f"{Fore.RESET}")

        sys.exit(0)

    if arg1 == "-e":  # Erase
        if input("Are you sure you want to DELETE all of your saved boards?\n"
                 "Favourites will not be affected. [y/n] ").lower() == "y":
            for file in os.listdir(BOARDS_PATH):
                # Remove each file but leave the folder
                os.remove(os.path.join(BOARDS_PATH, file))

            print(f"{Fore.GREEN}SUCCESS: {Fore.RESET}Files deleted.")
        sys.exit(0)

    if arg1 == "-f" and len(sys.argv) > 2:  # Favourite
        fav_file = f"{sys.argv[2]}{'.gol' if sys.argv[2][-4:] != '.gol' else ''}"

        if check_origin(fav_file) == BOARDS_PATH:
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

        if check_origin(fav_file) == FAVOURITES_PATH:
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

            else:
                print("\nNo files were moved.")
                sys.exit(0)

        print(f"{Fore.RED}ERROR: {Fore.RESET}File \"{fav_file}\" "
                "could not be found. No files were moved.")

        sys.exit(1)

    if arg1 == "-n" and len(sys.argv) > 2:  # New file
        # Set the name of the file to override

        overwrite_file: str = add_extension(sys.argv[2])
        origin = check_origin(overwrite_file)
        if origin == BOARDS_PATH:
            # File exists already in boards folder
            if input("This file already exists. "
                     f"Do you want to override \"{overwrite_file}\"? "
                      "This will delete the old one. [y/n] ").lower() == "y":
                print()
                # Delete old file
                os.remove(os.path.join(origin, overwrite_file))
                manually_create_level(overwrite_file)

        elif origin == FAVOURITES_PATH:
            # File exists already in favourites folder
            print(f"A file called \"{overwrite_file}\" already exists in your favourites.")
            overwrite_file = overwrite_file[:-4] + "(1)" + overwrite_file[-4:]  # Add (1) to name
            print(f"A file called \"{overwrite_file}\" will be created instead.")

            manually_create_level(overwrite_file)

        else:
            # File doesn't exist yet
            manually_create_level(overwrite_file)

        sys.exit(0)

    if arg1 == "-d" and len(sys.argv) > 2:  # Delete
        # Set the name of the file to delete
        file_to_delete = f"{sys.argv[2]}{'.gol' if sys.argv[2][-4:] != '.gol' else ''}"
        try:
            os.remove(os.path.join(check_origin(file_to_delete), file_to_delete))
            print(f"{Fore.GREEN}SUCCESS: {Fore.RESET}File deleted successfully.")
        except TypeError:
            # Because of the None return in check_origin
            print(f"{Fore.RED}ERROR: {Fore.RESET}The filename \"{file_to_delete}\" "
                  "doesn't seem to exist, so nothing was deleted.")
        sys.exit(0)

    if len(sys.argv) > 2 and any(arg == "-c" for arg in sys.argv):  # Char
        # Assign to the char after arg
        board_filler = sys.argv[sys.argv.index("-c") + 1]

        finish = True

        while len(board_filler) != 1:
            board_filler = input("Exactly ONE character can fill the board. Enter new character: ")

    if len(sys.argv) > 2 and any(arg == "-t" for arg in sys.argv):  # Time
        timeout = sys.argv[sys.argv.index("-t") + 1]
        while not timeout.replace(".", "", 1).isdigit():
            timeout = input("Enter a float or int as a board timeout: ")

        timeout = float(timeout)
        finish = True

    if sys.argv[1][0] == "-" and not finish:  # Invalid
        print(f"{Fore.RED}ERROR: {Fore.RESET}"
              "Invalid argument. Filenames cannot start with a hyphen. See -h for help.")
        sys.exit(1)

    return board_filler, timeout  # Default filler, default interval


def display_welcome() -> None:
    """Print some welcome words and infos regarding the game.
    
    Credit to https://fsymbols.com/generators/carty/ for the ASCII art.
    """
    clear()
    print("""
░░░░░██╗░█████╗░██╗░░██╗███╗░░██╗  ░█████╗░░█████╗░███╗░░██╗░██╗░░░░░░░██╗░█████╗░██╗░░░██╗██╗░██████╗
░░░░░██║██╔══██╗██║░░██║████╗░██║  ██╔══██╗██╔══██╗████╗░██║░██║░░██╗░░██║██╔══██╗╚██╗░██╔╝╚█║██╔════╝
░░░░░██║██║░░██║███████║██╔██╗██║  ██║░░╚═╝██║░░██║██╔██╗██║░╚██╗████╗██╔╝███████║░╚████╔╝░░╚╝╚█████╗░
██╗░░██║██║░░██║██╔══██║██║╚████║  ██║░░██╗██║░░██║██║╚████║░░████╔═████║░██╔══██║░░╚██╔╝░░░░░░╚═══██╗
╚█████╔╝╚█████╔╝██║░░██║██║░╚███║  ╚█████╔╝╚█████╔╝██║░╚███║░░╚██╔╝░╚██╔╝░██║░░██║░░░██║░░░░░░██████╔╝
░╚════╝░░╚════╝░╚═╝░░╚═╝╚═╝░░╚══╝  ░╚════╝░░╚════╝░╚═╝░░╚══╝░░░╚═╝░░░╚═╝░░╚═╝░░╚═╝░░░╚═╝░░░░░░╚═════╝░

░██████╗░░█████╗░███╗░░░███╗███████╗  ░█████╗░███████╗  ██╗░░░░░██╗███████╗███████╗
██╔════╝░██╔══██╗████╗░████║██╔════╝  ██╔══██╗██╔════╝  ██║░░░░░██║██╔════╝██╔════╝
██║░░██╗░███████║██╔████╔██║█████╗░░  ██║░░██║█████╗░░  ██║░░░░░██║█████╗░░█████╗░░
██║░░╚██╗██╔══██║██║╚██╔╝██║██╔══╝░░  ██║░░██║██╔══╝░░  ██║░░░░░██║██╔══╝░░██╔══╝░░
╚██████╔╝██║░░██║██║░╚═╝░██║███████╗  ╚█████╔╝██║░░░░░  ███████╗██║██║░░░░░███████╗
░╚═════╝░╚═╝░░╚═╝╚═╝░░░░░╚═╝╚══════╝  ░╚════╝░╚═╝░░░░░  ╚══════╝╚═╝╚═╝░░░░░╚══════╝
""")
    if input("Woud you like to display the instructions? [y/n] ").lower() != "y":
        clear()
        return

    print()
    print(f"""
{Back.LIGHTWHITE_EX}{Fore.BLACK}Overviev:{Back.RESET}{Fore.RESET}
The Game of Life is a cellular automaton devised by mathematician John Conway in 1970.
It's a zero-player game, meaning its evolution is determined by its initial state, with no further input.
The game is played on a grid of cells, each of which can be in one of two states: alive or dead.
Each generation is created by applying the game rules simultaneously to every cell on the board,
so that births and deaths occur simultaneously.

{Back.LIGHTWHITE_EX}{Fore.BLACK}Rules:{Back.RESET}{Fore.RESET}
Births:    A dead cell with exactly three live neighbors becomes alive in the next generation.
Survivals: A live cell with two or three live neighbors survives to the next generation.
Deaths:    A live cell with fewer than two live neighbors dies due to underpopulation,
                and a live cell with more than three live neighbors dies due to overpopulation.

{Back.LIGHTWHITE_EX}{Fore.BLACK}Additional information:{Back.RESET}{Fore.RESET}
Also read the README.md file for more information or launch the game with the "-h" command line argument.
This game looks and works best in the new windows terminal application
    (the default terminal app for Windows 11)
Try to pinch to zoom out for more cells in the simulation when using an auto-generated board.
""")
    input("Press [Enter] to continue to the game.")
    clear()


def get_start_board() -> list[list[bool]]:
    """Handle and return a board based on the command line arguments."""
    # Get filename to import from command line args, avoiding special args
    filename: str = sys.argv[1] if len(sys.argv) > 1 and "-" not in sys.argv[1] else ""

    if filename:
        try:
            # Try to import the file from the specified filepath
            local_board = import_from_file(filename)

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
            if input("Would you like to delete the corrupted file? [y/n] ").lower() == "y":
                # Delete invalid file
                filename = add_extension(filename)
                # Look in both the boards and the favourites folder
                os.remove(os.path.join(check_origin(filename), filename))
                print(f"{Fore.GREEN}SUCCESS: {Fore.RESET}{filename} deleted successfully")

            sys.exit(1)

    else:
        # No args, full terminal boards will be created
        local_board = generate_random_board()

    return local_board


def controlled_input(input_string: str, max_len: int) -> list[str]:
    """Input function but with max length

    Automatically returns and goes on to the next line when the specified
    input length has been reached.
    Still allows for Ctrl+C to interrupt the program.
    This function was written with the help of ChatGPT.

    WARNING: This only works on Windows devices.
    """
    input_chars: list[str] = []
    print(input_string, end="", flush=True)

    while True:
        if msvcrt.kbhit():  # React to keyboard input
            # Get typed character from keyboard and decode it
            char = msvcrt.getwch()
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
        # Terminal rendering doesn't like fullscreen, make place for generation count
        height = terminal.lines - 3
        # One cell is 2 chars wide, make place for separator
        width = terminal.columns // 2 - 1

    for _ in range(height):
        # Generate a line of bools
        generated_line = [(random.random() <= 0.5) for _ in range(width)]
        local_board.append(generated_line)

    return local_board


def import_from_file(filepath: str) -> list[list[bool]]:
    """Turns a file into a proper list and checks the validity of the board."""
    local_board: list[list[bool]] = []
    line: str = "PLACEHOLDER"

    # Add file extension if it wasn't provided
    filepath = add_extension(filepath)

    with open(os.path.join(check_origin(filepath), filepath), "r", encoding="utf-8") as fp:
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


def add_extension(filename: str) -> str:
    """Add the .gol extension to a file if not present already."""
    return filename + (".gol" if filename[-4:] != ".gol" else "")


def manually_create_level(filename: str="") -> list[list[bool]]:
    """Create a level according to user specifications.

    The new level will be saved in a .gol file as characters.
    Print a success message at the end if all worked well.
    """
    if MSVCRT_ERR:
        # Invalid OS or python version
        print(f"""
{Fore.RED}FATAL ERROR{Fore.RESET}
This part of the program cannot be accessed either due to an invalid Python version
or not running the game on a Windows environment.

Please restart the game either on a Windows device
or using Python 3.12 or 3.11 (the game is tested for those versions).""")
        sys.exit(1)

    local_board: list[list[str]] = []
    filename = add_extension(filename)

    with open(os.path.join(BOARDS_PATH, filename), "w", encoding="utf-8") as fp:
        if check_origin(filename) == FAVOURITES_PATH:
            print(f"A file called \"{filename}\" is already in your favourites.")
            filename = filename[:-4] + "(1)" + filename[-4:]  # Add ending (1) to filename
            print(f"A file called \"{filename}\" will be created instead.")

        print()
        # Get parameters for the board from the user
        while True:
            width: str = input("Enter board width (cells): ")
            if not width.isnumeric() or int(width) <= 1:
                print("Minimum value is 2. Please only write numbers\n")
                continue

            height: str = input("Enter board height (cells): ")
            if not height.isnumeric() or int(height) <= 1:
                print("Minimum value is 2. Please only write numbers\n")
                continue

            height, width = int(height), int(width)
            break

        print()
        # Actually get and save input
        for i in range(height):
            # Format and write chars entered by user
            line: list[str] = controlled_input(f"Enter line No. {i + 1}: ", width)
            # Directly convert input to bool values
            processed_input = [not char == " " for char in line]
            local_board.append(processed_input)

            fp.write("".join(line))
            if i != height - 1:
                # Don't write last newline
                fp.write("\n")

        print(f"\n{Fore.GREEN}SUCCESS: {Fore.RESET}File created successfully!")

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


def update_board(board: list[list[bool]], count: int) -> list[list[bool]]:
    """Update the board according to the rules of the Game of Life.
    
    Credit to Mizipor on StackOverflow for the non-blocking input.
    Link to the thread: https://stackoverflow.com/questions/2408560/non-blocking-console-input
    """
    # Initialize a board where all cells are dead
    new_board: list[list[bool]] = [[False] * len(board[0]) for _ in range(len(board))]
    live_cells = 0  # To check if entire board is dead

    for i, _ in enumerate(board):
        for j, counter in enumerate(board[i]):
            live_neighbors = count_neighbors(board, i, j)

            # Apply Game of Life rules
            #     live cell has 2 or 3 neighbours           cell is a birth cell -> 3 neighbours
            if (counter and (live_neighbors in (2, 3))) or (not counter and live_neighbors == 3):
                new_board[i][j] = True
                live_cells += 1

    if live_cells == 0:
        # Entire board is dead, end the game with the amount of generations passed
        end_game(count)

    if not MSVCRT_ERR and msvcrt.kbhit():
        # bkhit() check only works on Windows
        if msvcrt.getch() == b"\r":
            # User has pressed [Enter] to exit the game mid-simulation.
            end_game(count)


    return new_board


def print_board(local_board: list[list[bool]], gen_count: int, character: str = " ") -> None:
    """Print the current state of the board. Display the number of passed generations.

    Colorama is used to draw colored characters.
    Live cells are displayed as green.
    The specified character is used to fill the cells, default is empty.

    Screen flickering can occur, but that can't be avoided while not fundamentally
    changing the structure of the program. This is due to how most terminal
    applications handle output, which is line by line. When the ouput doesn't
    happen to be synchronized with the monitor refresh rate, flickering can't be
    avoided.
    """
    # Initialize buffer to avoid screen flickering for bigger boards
    buffered_board = ""

    clear()  # Clear the terminal

    for row in local_board:
        for cell in row:
            # Color only if cell is alive
            if cell:
                buffered_board += f"{Back.GREEN}{2 * character}{Back.RESET}"
            else:
                buffered_board += 2 * character
        buffered_board += "|\n"  # Separator and newline after row
    buffered_board += "-" * len(local_board[0]) * 2 + "|"  # Add bottom separator
    buffered_board += f"\nGeneration No. {gen_count}"

    # Print only at the end to minimize flickering
    print(buffered_board)


def end_game(count: int = -1) -> None:
    """Finish the game and display the number of passed generations."""
    print("""
░██████╗██╗███╗░░░███╗██╗░░░██╗██╗░░░░░░█████╗░████████╗██╗░█████╗░███╗░░██╗  ░█████╗░██╗░░░██╗███████╗██████╗░
██╔════╝██║████╗░████║██║░░░██║██║░░░░░██╔══██╗╚══██╔══╝██║██╔══██╗████╗░██║  ██╔══██╗██║░░░██║██╔════╝██╔══██╗
╚█████╗░██║██╔████╔██║██║░░░██║██║░░░░░███████║░░░██║░░░██║██║░░██║██╔██╗██║  ██║░░██║╚██╗░██╔╝█████╗░░██████╔╝
░╚═══██╗██║██║╚██╔╝██║██║░░░██║██║░░░░░██╔══██║░░░██║░░░██║██║░░██║██║╚████║  ██║░░██║░╚████╔╝░██╔══╝░░██╔══██╗
██████╔╝██║██║░╚═╝░██║╚██████╔╝███████╗██║░░██║░░░██║░░░██║╚█████╔╝██║░╚███║  ╚█████╔╝░░╚██╔╝░░███████╗██║░░██║
╚═════╝░╚═╝╚═╝░░░░░╚═╝░╚═════╝░╚══════╝╚═╝░░╚═╝░░░╚═╝░░░╚═╝░╚════╝░╚═╝░░╚══╝  ░╚════╝░░░░╚═╝░░░╚══════╝╚═╝░░╚═╝
""")
    if count >= 0:
        print(f"Your game lasted {count} generation{'s' if count > 1 else ''}.")
    input("\nPress [Enter] to exit the game.")
    clear()
    # Exit program with code 0
    sys.exit(0)

# Run the following even if module is imported
set_dir_and_os()
# Path to where the boards are stored
BOARDS_PATH: str = os.path.abspath(os.path.join("..", "boards"))
# Favourite boards
FAVOURITES_PATH: str = os.path.abspath(os.path.join("..", "favourites"))

# Make necessary directories if they don't exist already
os.makedirs(BOARDS_PATH, exist_ok=True)
os.makedirs(FAVOURITES_PATH, exist_ok=True)

# Only run the following if program is called explicitly
if __name__ == "__main__":
    print("-" * 20)  # Visual separator

    BACKGROUND_CHAR, TIMEOUT = handle_special_args()  # Check special args first
    display_welcome()  # Only if no special args were called

    # Initial configuration comes either from the user or is randomly generated
    current_board: list[list[bool]] = get_start_board()
    # Avoid stuck screens that only include still lives
    last_board: list[list[bool]] = []
    num_generations: int = 0  # Keep track of how many generations passed

    print("Starting simulation...")
    sleep(1.5)

    if MSVCRT_ERR:
        # Warn the user that a part of the functionality won't work
        input("""
Because you're either running an older python version or you're on a Unix OS, you can only
interrupt the simulation using [Ctrl/Cmd + C] and not by pressing [Enter].
Like this, you won't be able to see the end stats, the game will just \"crash\".

Press [Enter] to continue.""")

    # Main game loop
    while last_board != current_board:
        num_generations += 1
        print_board(current_board, num_generations, BACKGROUND_CHAR)
        last_board = current_board
        current_board = update_board(current_board, num_generations)
        sleep(TIMEOUT)

    end_game(num_generations)
