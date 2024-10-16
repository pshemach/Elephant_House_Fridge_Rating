import torch
import torchvision
from torchvision.transforms import transforms
import yaml
from PIL import Image
import torch.nn as nn


# Load config file
def load_config(config_path="config/config.yaml"):
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    return config


config = load_config()  # Load the configuration

# Device configuration
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Define the categories
categories = ["not_rated", "rated"]


# Define the model architecture
def load_rating_model():
    model = torchvision.models.efficientnet_b0(pretrained=True).to(device)
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.2, inplace=True),
        nn.Linear(in_features=1280, out_features=len(categories), bias=True),
    ).to(device)

    # Load the model's state dictionary from the path in the config
    model_path = config["model"]["rating_model_path"]
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()
    return model


# Transformation pipeline
transform = transforms.Compose(
    [
        transforms.Resize((640, 640)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)


def get_rating(image: Image.Image):
    """
    Predicts the rating of the image (not_rated or rated).
    """
    # Transform the image
    image_tensor = transform(image).unsqueeze(0).to(device)

    # Load the rating model
    model = load_rating_model()

    # Perform prediction
    with torch.no_grad():
        output = model(image_tensor)
        predicted_class = torch.argmax(output, dim=1).item()

    return categories[predicted_class]
