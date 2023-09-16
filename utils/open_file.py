import os

def open_file(path: str):
    """Opens file depends on which platform the user uses."""
    if os.name == 'nt':  # Windows
        os.startfile(path)
    else:  # Other platforms
        subprocess.run(['xdg-open', path])