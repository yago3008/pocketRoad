import io
import torch
import torch.nn as nn
from torchvision import models, transforms
from fastapi import FastAPI, File, UploadFile
from PIL import Image
import uvicorn
import json

# -----------------------------
# CONFIGURAÇÕES
# -----------------------------

MODEL_PATH = "resnet50_cars.pth"
CLASSES_PATH = "classes.txt"   # arquivo contendo uma classe por linha

# Carrega classes
with open(CLASSES_PATH, "r", encoding="utf-8") as f:
    class_names = [line.strip() for line in f.readlines()]

num_classes = len(class_names)

# -----------------------------
# CARREGA O MODELO
# -----------------------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = models.resnet50(weights=None)
model.fc = nn.Linear(model.fc.in_features, num_classes)
model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
model.eval()
model.to(device)

# -----------------------------
# TRANSFORMAÇÕES
# -----------------------------
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

# -----------------------------
# API
# -----------------------------
app = FastAPI()


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Lê imagem
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

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

# -----------------------------
# RUN (modo desenvolvimento)
# -----------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
