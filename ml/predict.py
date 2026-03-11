from pathlib import Path

import torch
from PIL import Image
from torchvision import transforms

from .model import FLOWER_CLASSES, load_trained_model

_model = None


def _get_model():
    global _model
    if _model is None:
        _model = load_trained_model()
    return _model


def _build_transform():
    return transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )


def predict_flower(image_field_file):
    model = _get_model()
    transform = _build_transform()

    image_field_file.seek(0)
    image = Image.open(image_field_file).convert('RGB')
    tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        logits = model(tensor)
        probabilities = torch.softmax(logits, dim=1)[0]
        confidence, class_idx = torch.max(probabilities, dim=0)

    class_name = FLOWER_CLASSES[class_idx.item()]
    return class_name, float(confidence.item() * 100)
