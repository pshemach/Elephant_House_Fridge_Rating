from PIL import Image
from eleRating.models.rating_model import get_rating
from eleRating.models.segmentation import get_products
from eleRating.utils import load_config
from eleRating.constant import CONFIG_PATH

config = load_config(config_path=CONFIG_PATH)


def run_prediction(image_path):
    """
    Runs the prediction pipeline locally for a single image.
    """
    image = Image.open(image_path).convert("RGB")

    # Step 1: Get initial rating prediction
    rating = get_rating(image)

    if rating == config["instances"]["classify_cls"][0]:
        return config["output_cat"][0]

    # Step 2: Use segmentation to get product classes
    classes = get_products(image)

    # Step 3: Decide final rating
    if (
        config["instances"]["segment_ins"]["products"][0] in classes
        and config["instances"]["segment_ins"]["products"][1] not in classes
    ):
        return config["output_cat"][1]
    elif (
        config["instances"]["segment_ins"]["products"][0] in classes
        and config["instances"]["segment_ins"]["products"][1] in classes
    ):
        return config["output_cat"][2]
    else:
        return config["output_cat"][3]
