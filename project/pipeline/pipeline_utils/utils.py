import pathlib


def get_directory_absolute_path():
    """
    Return the absolute path of the root project based on this file.
    """
    return pathlib.Path(__file__).parent.parent.parent.parent.resolve()
