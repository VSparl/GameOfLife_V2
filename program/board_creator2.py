"""Separate module to specifically create boards, based on the main.py program."""
import sys
# Prevent pyhon from creating pycache when importing main
sys.dont_write_bytecode = True
from main import add_extension, manually_create_level

if len(sys.argv) == 1:
    # No arguments
    print("Usage: py board_creator.py [filename]")
    sys.exit(1)

# Complete filename extension if needed
filename = add_extension(sys.argv[1])

manually_create_level(filename)
