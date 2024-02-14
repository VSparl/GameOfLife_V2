import os
import sys
import webbrowser
from tkinter import filedialog
from time import sleep

def end():
    """End the program by opening the README page on GitHub."""
    # Open the readme in the default browser
    print("-" * 20)
    print("All done! Check your browser for the GitHub README page of the project.")
    sleep(1)
    webbrowser.open("https://github.com/VSparl/GameOfLife_V2?tab=readme-ov-file#conways-game-of-life", new=2)
    sys.exit(0)

# Install colorama if needed
print("Checking for colorama install...")
try:
    import colorama
    print("Found colorama install.")

except ImportError as ex:
    # Colorama couldn't be imported
    try:
        if input("Colorama not found. Do you want to install it? [y/n] ").lower() == "y":
            # User wants to install colorama through script, try to install it
            if os.system(f"{sys.executable} -m pip install colorama") != 0:
                # os.system returned a non-zero exit code, something went wrong
                raise RuntimeError("Error installing Colorama. Please install it manually.") from ex

            import colorama
    except Exception as e:
        # Catch any other errors
        print(f"Error: {e}")

# Navigate to the correct directory (got help from ChatGPT with the Tkinter part)
print()
if input("Do you want to clone the GitHub repository onto your machine?\n"
         "You will be able to select your directory. [y/n] ").lower() != "y":
    end()

# Ask user for directory where the repo should be saved
print("A file dialog should have popped up somewhere. Please select your desired directory.")
save_path = filedialog.askdirectory(title="Game of Life target folder")
if not save_path:
    print()
    print("You pressed cancel, nothing will be cloned.\n"
          "Run this program again to set up the repo.")
    end()

# Clone the GitHub repo
os.chdir(save_path)
print("\nAttempting to clone the GitHub repository...")
clone_response = os.system("git clone https://github.com/VSparl/GameOfLife_V2")
if clone_response != 0:
    # Non-zero return code
    print("Something went wrong with git. Please refer to the README for a manual install.")

end()
