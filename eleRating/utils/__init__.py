from PIL import Image

def load_image(image_path):
    """Loads an image and returns the PIL Image object."""
    return Image.open(image_path).convert('RGB')