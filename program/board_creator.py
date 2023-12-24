"""A standalone version of the integrated level editor from the main program.

Here you can make your own board configurations on demand, as opposed to only
getting to the editor via an error in the full game.
"""
import msvcrt
import sys
import os


def controlled_input(input_string: str, max_len: int) -> list:
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
            char = msvcrt.getch().decode("utf-8")
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


filename: str = input("Enter filename: ")
WIDTH: int = int(input("How wide? (chars) "))
HEIGHT: int = int(input("How high? (chars) "))

if filename[-4:] != ".gol":
    filename += ".gol"

with open(os.path.join("..", "boards", filename), "w", encoding="utf-8") as fp:
    for i in range(HEIGHT):
        # Format and write chars entered by user
        fp.write("".join(controlled_input(f"Enter line No. {i + 1}: ", WIDTH)))

        if i != HEIGHT - 1:
            # Don't write last newline
            fp.write("\n")

print(f"Successfully created file under \"boards\{filename}.gol\"")
sys.exit(0)
