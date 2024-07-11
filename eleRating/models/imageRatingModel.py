import torch
import torchvision
from torchvision.transforms import transforms
from PIL import Image
import torch.nn as nn


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

categories = ['not_rated', 'rated']
output_shape = len(categories)


model = torchvision.models.efficientnet_b0(pretrained=True).to(device)

model.classifier = nn.Sequential(
    nn.Dropout(p=0.2, inplace=True),
    nn.Linear(in_features=1280, out_features=output_shape, bias=True)
  ).to(device)

model_path = r'C:\Users\PC\Desktop\test\Elephant_House_Fridge_Rating\research\mobilenet_transfer_learning.pth'
model.load_state_dict(torch.load(model_path, map_location=device))
model.eval()

def predict_rating(image_tensor):
    img_tensor = image_tensor.to(device)
    
    with torch.no_grad():
        output = model(img_tensor)
        predicted_class = torch.argmax(output, dim=1).item()
        return categories[predicted_class]