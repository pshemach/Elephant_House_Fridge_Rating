import yaml
from ultralytics import YOLO
from eleRating.constant import SEGMENTATION_CONF, IS_SAVE_SEGMENTATION


# Load the config file
def load_config(config_path="config/config.yaml"):
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    return config


config = load_config()  # Load the configuration


def get_products(image):
    """
    Use the segmentation model to detect products in the fridge.
    :param image: Input image (PIL Image or similar)
    :return: A set of unique detected product classes
    """
    # Load the YOLO segmentation model using the path from the config file
    model_path = config["model"]["segmentation_path"]  # Fetch model path from config
    model = YOLO(model_path)

    # Get results from the model
    results = model.predict(image, save=IS_SAVE_SEGMENTATION, conf=SEGMENTATION_CONF)

    # Collect detected classes
    detected_classes = []
    for result in results:
        if result.boxes is not None:
            for box in result.boxes:
                class_idx = int(box.cls)
                detected_classes.append(result.names[class_idx])

    # Return unique product classes
    unique_classes = set(detected_classes)
    return unique_classes
