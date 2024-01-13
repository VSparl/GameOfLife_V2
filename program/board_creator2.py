"""Separate module to specifically create boards, based on the main.py program."""
import sys
import os

# Prevent pyhon from creating pycache when importing main
sys.dont_write_bytecode = True
try:
    from main import (add_extension,
                      manually_create_level,
                      check_origin,
                      BOARDS_PATH)
except ImportError:
    print("You didn't clone the GitHub repo properly or you deleted the main.py program.\n"
          "Please refer to the \"Installation\" section of the README for more Information.")
    sys.exit(1)

os.system("cls")
if len(sys.argv) != 2:
    # None or too many arguments
    print("Usage: py board_creator.py [filename]")
    sys.exit(1)

filename = add_extension(sys.argv[1])

# Handle existing files
origin = check_origin(filename)
if origin is not None:
    # File exists
    if origin == BOARDS_PATH:
        if input(f"\"{filename}\" already exists. "
                 "Do you want to override it? [y/n] ").lower() == "y":
            manually_create_level(filename)
        else:
            sys.exit(0)

    else:  # origin = FAVOURITES_PATH
        print(f"A file called \"{filename}\" already exists in your favourites.")
        filename = filename[:-4] + "(1)" + filename[-4:]  # Add (1) to name
        print(f"A file called \"{filename}\" will be created instead.")
        manually_create_level(filename)
