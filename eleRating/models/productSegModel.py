from ultralytics import YOLO

model_path = r'C:\Users\PC\Desktop\test\Elephant_House_Fridge_Rating\eleRating\models\my_model_2.pt'

model = YOLO(model_path)

def get_products(image_path):
    results = model.predict(image_path)
    detected_classes=[]
    for result in results:
        if result.boxes is not None:
            for box in result.boxes:
                class_idx = int(box.cls)
                detected_classes.append(result.names[class_idx])

    unique_classes = set(detected_classes)
    print(unique_classes)
    return unique_classes

# image_path = r'C:\Users\PC\Desktop\test\Elephant_House_Fridge_Rating\data\rated_6.jpg'

# products = get_products(image_path)

# print(products)