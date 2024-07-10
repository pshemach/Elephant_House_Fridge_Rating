import torch
import torchvision
from torchvision.transforms import transforms
from PIL import Image
import torch.nn as nn


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

categories = ['rated', 'not_rated']
output_shape = len(categories)

transform = transforms.Compose([
    transforms.Resize((640,640)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

model = torchvision.models.efficientnet_b0(pretrained=True).to(device)

model.classifier = nn.Sequential(
    nn.Dropout(p=0.2, inplace=True),
    nn.Linear(in_features=1280, out_features=output_shape, bias=True)
  ).to(device)

model.load_state_dict(torch.load('mobilenet_transfer_learning.pth', map_location=device))
model.eval()

def predict_rating(image_path):
    img = Image.open(image_path).convert('RGB')
    img_tensor = transform(img).unsqueeze(0)
    img_tensor = img_tensor.to(device)
    
    with torch.no_grad():
        output = model(img_tensor)
        predicted_class = torch.argmax(output, dim=1).item()
        return categories[predicted_class]
    

# image_path = 'example_image.jpg'

# predicted_rating = predict_rating(image_path)

# print(f'Predicted rating: {predicted_rating}')




