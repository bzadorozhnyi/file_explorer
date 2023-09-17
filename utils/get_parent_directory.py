import os


def get_parent_directory(current_directory: str) -> str:
    return os.path.dirname(current_directory)
