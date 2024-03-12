import os
import shutil


def empty_folder(folder_path):
    """
    Empties all the contents of the specified folder, including files and subdirectories.

    Parameters:
    - folder_path: A string representing the path to the folder to be emptied.
    """
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)  # Removes files and symbolic links
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)  # Removes directories and their contents
        except Exception as e:
            print(f"Failed to delete {item_path}. Reason: {e}")
