from PIL import Image
from eleRating.models.rating_model import get_rating
from eleRating.models.segmentation import get_products


def run_prediction(image_path):
    """
    Runs the prediction pipeline locally for a single image.
    """
    image = Image.open(image_path).convert("RGB")

    # Step 1: Get initial rating prediction
    rating = get_rating(image)

    if rating == "not_rated":
        return "Not Rated"

    # Step 2: Use segmentation to get product classes
    classes = get_products(image)

    # Step 3: Decide final rating
    if "elephant-product" in classes and "other" not in classes:
        return "Good"
    elif "elephant-product" in classes and "other" in classes:
        return "Bad"
    else:
        return "Worst"
