from pathlib import Path

import torch
import torch.nn as nn
from torchvision import models

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_WEIGHTS_PATH = BASE_DIR / 'ml' / 'flower_model.pth'

FLOWER_CLASSES = [
    'Ромашка',
    'Одуванчик',
    'Роза',
    'Подсолнух',
    'Тюльпан',
]


def build_model(num_classes: int) -> nn.Module:
    model = models.resnet18(weights=None)
    in_features = model.fc.in_features
    model.fc = nn.Linear(in_features, num_classes)
    return model


def load_trained_model(weights_path: Path = MODEL_WEIGHTS_PATH) -> nn.Module:
    if not weights_path.exists():
        raise FileNotFoundError(
            f"Файл весов не найден: {weights_path}. \
Скачайте или обучите модель и положите веса в ml/flower_model.pth"
        )

    model = build_model(len(FLOWER_CLASSES))
    state = torch.load(weights_path, map_location='cpu')
    model.load_state_dict(state)
    model.eval()
    return model
