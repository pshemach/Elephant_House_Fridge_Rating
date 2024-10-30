import os

ALLOWED_FILE_EXTENSIONS = {"jpg", "jpeg", "png"}

CONFIG_PATH = "config/config.yaml"

SEGMENTATION_CONF = 0.5
IS_SAVE_SEGMENTATION = False
HOME = os.getcwd()
IMAGE_SAVE_DIR = "static/results"
IMAGE_SAVE_NAME = "segmentation_result.jpg"
UPLOAD_IMAGE_DIR = "static/uploads"

TEMP_FILE_MAX_AGE = 30
