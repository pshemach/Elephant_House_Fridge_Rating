from PIL import Image
from eleRating.constant import ALLOWED_FILE_EXTENSIONS

def load_image(image_path):
    """Loads an image and returns the PIL Image object."""
    return Image.open(image_path).convert('RGB')


def is_allowed(filename):
    """
    Check if the file has an allowed extension.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_FILE_EXTENSIONS
