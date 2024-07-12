import torch
import torchvision
from torchvision.transforms import transforms
from PIL import Image
import torch.nn as nn
from eleRating.models.imageRatingModel import predict_rating
from eleRating.models.productSegModel import get_products


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

transform = transforms.Compose([
    transforms.Resize((640,640)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])


def get_prediction(image_path):
    image = Image.open(image_path).convert('RGB')
    image_tensor = transform(image).unsqueeze(0)
    image_selection = predict_rating(image_tensor=image_tensor)
    if image_selection == 'not_rated':
        return image_selection
    elif image_selection == 'rated':
        classes = get_products(image_path=image)
        if 'elephant-product' in classes and 'other' not in classes:
            return 'Good'
        elif 'elephant-product' in classes and 'other' in classes:
            return 'Bad'
        elif 'elephant-product' not in classes:
            return 'Worst'