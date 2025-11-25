#from models.cardex import Cardex
#from config.database import db
#from services.utils_service import UtilsService
#from exceptions.exceptions import (
#    ManualValidationIsNecessary
#)
import io
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image

# -------------------------------------------------
# CONFIGURAÇÕES
# -------------------------------------------------

MODEL_PATH = r"C:\Users\yago.martins.SOOW\Documents\pocketRoad\pocketroad\pocketRoad\AI Training\resnet50_cars.pth"
CLASSES_PATH = r"C:\Users\yago.martins.SOOW\Documents\pocketRoad\pocketroad\pocketRoad\AI Training\classes.txt"   # arquivo contendo uma classe por linha

# Carrega classes
with open(CLASSES_PATH, "r", encoding="utf-8") as f:
    class_names = [line.strip() for line in f.readlines()]

num_classes = len(class_names)

# -------------------------------------------------
# CARREGA O MODELO
# -------------------------------------------------

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = models.resnet50(weights=None)
model.fc = nn.Linear(model.fc.in_features, num_classes)

model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
model.eval()
model.to(device)

# -------------------------------------------------
# TRANSFORM (pré-processamento da imagem)
# -------------------------------------------------

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

class AIService:
    @staticmethod
    def predict_car(image):
        file_bytes = image.read()
        # Converte para PIL
        image = Image.open(io.BytesIO(file_bytes)).convert("RGB")

        # Preprocessa
        img_tensor = transform(image).unsqueeze(0).to(device)

        # Predição
        with torch.no_grad():
            outputs = model(img_tensor)
            probabilities = torch.softmax(outputs, dim=1)

        prob, idx = torch.max(probabilities, dim=1)
        predicted_class = class_names[idx.item()]
        accuracy = prob.item()

        return {
            "predicted_car": predicted_class,
            "confidence": round(float(accuracy), 4)
        }

        
