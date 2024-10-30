import yaml
import os
from PIL import Image
from eleRating.constant import ALLOWED_FILE_EXTENSIONS
import uuid
import shutil
import tempfile
import time


def load_image(image_path):
    """Loads an image and returns the PIL Image object."""
    return Image.open(image_path).convert("RGB")


def is_allowed(filename):
    """
    Check if the file has an allowed extension.
    """
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_FILE_EXTENSIONS
    )


# Load the config file
def load_config(config_path):
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    return config


def is_inside_fridge(object_bbox, fridge_bbox):
    """
    Checks if the object's bounding box is inside the fridge's bounding box.
    :param object_bbox: Tuple (x1, y1, x2, y2) for the object
    :param fridge_bbox: Tuple (x1, y1, x2, y2) for the fridge
    :return: True if the object is inside the fridge, False otherwise
    """
    obj_x1, obj_y1, obj_x2, obj_y2 = object_bbox
    fridge_x1, fridge_y1, fridge_x2, fridge_y2 = fridge_bbox

    # Check if the object's bounding box is within the fridge's bounding box
    if (
        obj_x1 >= fridge_x1
        and obj_y1 >= fridge_y1
        and obj_x2 <= fridge_x2
        and obj_y2 <= fridge_y2
    ):
        return True
    return False


def make_dir(path):
    # If the directory already exists, delete it and its contents
    if os.path.exists(path):
        shutil.rmtree(path)

    # Create a new directory
    os.makedirs(path)


def delete_previous_files(upload_dir, result_path):
    """
    Deletes previous uploaded image and result image from the directories.
    """
    # Remove previous uploaded image
    for filename in os.listdir(upload_dir):
        file_path = os.path.join(upload_dir, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    # Remove previous result image
    if os.path.exists(result_path):
        os.remove(result_path)


def make_temp_folder(root_dir):
    """
    Creates a unique temp directory per request
    """
    tem_dir = tempfile.mkdtemp(dir=root_dir)
    return tem_dir


def unique_filenameuni(image_name):
    """
    Generate a unique filename for the uploaded image
    """
    return f"{uuid.uuid4().hex}_{image_name}"


# Track previously created directories with their creation times
previous_temp_dirs = []


def create_temp_directory_with_age_limit(root_dir, max_age=60):
    """
    Deletes any temporary directories older than the specified max_age,
    then creates a new temporary directory.

    Parameters:
        root_dir (str): Path to the root directory where the temporary directory will be created.
        max_age (int): Maximum age in seconds. Directories older than this will be deleted.

    Returns:
        str: Path to the newly created temporary directory.
    """
    global previous_temp_dirs
    current_time = time.time()

    # Delete previous directories older than max_age
    for temp_dir, creation_time in previous_temp_dirs[:]:
        if current_time - creation_time > max_age:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)
                # print(f"Deleted old temporary directory: {temp_dir}")
            previous_temp_dirs.remove((temp_dir, creation_time))

    # Create a new temporary directory and store it with the current time
    new_temp_dir = tempfile.mkdtemp(dir=root_dir)
    previous_temp_dirs.append((new_temp_dir, current_time))
    # print(f"New temporary directory created at: {new_temp_dir}")

    return new_temp_dir
