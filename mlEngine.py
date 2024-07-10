import torch
import torchvision
from torchvision.transforms import transforms
from PIL import Image
import torch.nn as nn
from eleRating.models.imageRatingModel import predict_rating


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

transform = transforms.Compose([
    transforms.Resize((640,640)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])


def get_prediction(image_path):
    image_selection = predict_rating(image_path=image_path, transform=transform)
    if image_selection == 'not_rated':
        return image_selection
    elif image_selection == 'rated':
        return image_selection