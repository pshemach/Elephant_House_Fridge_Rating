from ultralytics import YOLO
import os
import cv2
from eleRating.utils import is_inside_fridge, load_config
from eleRating.constant import (
    SEGMENTATION_CONF,
    IS_SAVE_SEGMENTATION,
    IMAGE_SAVE_DIR,
    IMAGE_SAVE_NAME,
    CONFIG_PATH,
)


config = load_config(config_path=CONFIG_PATH)  # Load the configuration


# def get_products(image):
#     """
#     Use the segmentation model to detect products in the fridge.
#     :param image: Input image (PIL Image or similar)
#     :return: A set of unique detected product classes
#     """
#     # Load the YOLO segmentation model using the path from the config file
#     model_path = config["model"]["segmentation_path"]  # Fetch model path from config
#     model = YOLO(model_path)

#     # Get results from the model
#     results = model.predict(
#         image,
#         save=IS_SAVE_SEGMENTATION,
#         conf=SEGMENTATION_CONF,
#         save_dir=DIR,
#     )

#     # Collect detected classes
#     detected_classes = []
#     for result in results:
#         if result.boxes is not None:
#             for box in result.boxes:
#                 class_idx = int(box.cls)
#                 detected_classes.append(result.names[class_idx])
#         result_image = result.plot()
#         # cv2.imwrite(DIR, result_image)

#     # Return unique product classes
#     unique_classes = set(detected_classes)
#     return unique_classes


def get_products(image):
    """
    Use the segmentation model to detect products in the fridge.
    :param image: Input image (PIL Image or similar)
    :return: A set of unique detected product classes that are inside the fridge.
    """
    # Load the YOLO segmentation model using the path from the config file
    model_path = config["model"]["segmentation_path"]  # Fetch model path from config
    model = YOLO(model_path)

    # Get results from the model
    results = model.predict(
        image,
        save=IS_SAVE_SEGMENTATION,
        conf=SEGMENTATION_CONF,
        save_dir=IMAGE_SAVE_DIR,
    )

    # Initialize variables
    fridge_bbox = None
    detected_classes = []

    # First pass: Identify the fridge bounding box
    for result in results:
        if result.boxes is not None:
            for box in result.boxes:
                class_idx = int(box.cls)
                class_name = result.names[class_idx]
                x1, y1, x2, y2 = map(
                    int, box.xyxy[0]
                )  # Get the bounding box coordinates

                # If the detected object is a fridge, save its bounding box
                if class_name == config["instances"]["segment_ins"]["fridge"]:
                    fridge_bbox = (x1, y1, x2, y2)
                    break  # Exit the loop once the fridge is found

    # Second pass: Filter objects inside the fridge
    for result in results:
        if result.boxes is not None:
            for box in result.boxes:
                class_idx = int(box.cls)
                class_name = result.names[class_idx]
                x1, y1, x2, y2 = map(
                    int, box.xyxy[0]
                )  # Get the bounding box coordinates

                # Check if the object is inside the fridge's bounding box
                if (
                    fridge_bbox
                    and class_name in config["instances"]["segment_ins"]["products"]
                ):
                    if is_inside_fridge((x1, y1, x2, y2), fridge_bbox):
                        detected_classes.append(class_name)

        # Optionally save the result image
        result_image = result.plot()
        cv2.imwrite(os.path.join(IMAGE_SAVE_DIR, IMAGE_SAVE_NAME), result_image)

    # Return unique product classes that are inside the fridge
    unique_classes = set(detected_classes)
    return unique_classes
