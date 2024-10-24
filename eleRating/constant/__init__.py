import os

ALLOWED_FILE_EXTENSIONS = {"jpg", "jpeg", "png"}

CONFIG_PATH = "config/config.yaml"

SEGMENTATION_CONF = 0.5
IS_SAVE_SEGMENTATION = False
HOME = os.getcwd()
IMAGE_SAVE_DIR = os.path.join(HOME, "static/results")
IMAGE_SAVE_NAME = "segmentation_result.jpg"
IMAGE_SAVE_PATH = os.path.join(IMAGE_SAVE_DIR, IMAGE_SAVE_NAME)

UPLOAD_IMAGE_DIR = os.path.join(HOME, "static/uploads")
