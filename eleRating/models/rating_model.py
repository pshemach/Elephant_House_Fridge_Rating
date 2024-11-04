import torch
import torchvision
from torchvision.transforms import transforms
from PIL import Image
import torch.nn as nn
from eleRating.utils import load_config
from eleRating.constant import CONFIG_PATH

config = load_config(config_path=CONFIG_PATH)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
categories = config["instances"]["classify_cls"]

# Load the model globally
rating_model = None


def load_rating_model():
    global rating_model
    if rating_model is None:
        model = torchvision.models.efficientnet_b0()
        model.classifier = nn.Sequential(
            nn.Dropout(p=0.2, inplace=True),
            nn.Linear(in_features=1280, out_features=len(categories), bias=True),
        ).to(device)
        model_path = config["model"]["rating_model_path"]
        model.load_state_dict(torch.load(model_path, map_location=device))
        model.eval()
        rating_model = model


# Transformation pipeline
transform = transforms.Compose(
    [
        transforms.Resize((640, 640)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)


def get_rating(image: Image.Image):
    load_rating_model()  # Ensure model is loaded
    image_tensor = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        output = rating_model(image_tensor)
        predicted_class = torch.argmax(output, dim=1).item()

    return categories[predicted_class]
