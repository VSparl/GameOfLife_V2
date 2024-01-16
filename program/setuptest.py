import os
import sys

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

# Navigate to the correct directory

# something like using os.system() and just passing usr input directly until some specific thing is written (like ":q!" or sth)
# then agian such a try-statement mess to try to clone the repo, but maybe git isn't installed! :(
# in the end, maybe open the readme in a browser or something, might be nice idk I'm tired
