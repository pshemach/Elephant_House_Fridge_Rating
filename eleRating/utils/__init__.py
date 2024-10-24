import yaml
import os
from PIL import Image
from eleRating.constant import ALLOWED_FILE_EXTENSIONS


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
    if not os.path.exists(path):
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
