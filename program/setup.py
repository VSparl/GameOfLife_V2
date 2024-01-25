import os
import sys
import webbrowser
from tkinter import filedialog

# Install colorama if needed
print("Checking for colorama install...\n")
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
        print(f"Error: {e}")

# Navigate to the correct directory (got help from ChatGPT with the Tkinter part)
if input("Do you want to clone the GitHub repository onto your machine?\n"
         "You will be able to select your directory. [y/n] ").lower() != "y":
    sys.exit(0)

save_path = filedialog.askdirectory()
if not save_path:
    print("You pressed cancel, nothing will be cloned.\n"
          "Run this program again to set up the repo.")
    sys.exit(0)

os.chdir(save_path)

print("\nAttempting to clone the GitHub repository...")
clone_response = os.system("git clone https://github.com/VSparl/GameOfLife_V2")
if clone_response != 0:
    print("Something went wrong with git. Please refer to the README for a manual install.")

# Open the readme in the default browser
webbrowser.open("https://github.com/VSparl/GameOfLife_V2?tab=readme-ov-file#conways-game-of-life")
