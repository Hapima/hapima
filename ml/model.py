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


def _extract_state_dict(checkpoint):
    if isinstance(checkpoint, dict):
        if 'state_dict' in checkpoint:
            return checkpoint['state_dict']
        if 'model_state_dict' in checkpoint:
            return checkpoint['model_state_dict']
    return checkpoint


def load_trained_model(weights_path: Path = MODEL_WEIGHTS_PATH) -> nn.Module:
    if not weights_path.exists():
        raise FileNotFoundError(
            f'Файл весов не найден: {weights_path}. '
            'Скачайте или обучите модель и положите веса в ml/flower_model.pth'
        )

    checkpoint = torch.load(weights_path, map_location='cpu')
    state_dict = _extract_state_dict(checkpoint)

    out_features = state_dict.get('fc.weight', None)
    if out_features is not None and out_features.shape[0] != len(FLOWER_CLASSES):
        raise ValueError(
            'Несовместимые веса: в checkpoint последний слой имеет '
            f"{out_features.shape[0]} классов, а в FLOWER_CLASSES указано {len(FLOWER_CLASSES)}. "
            'Используйте веса, обученные на тех же классах цветков, '
            'или обновите FLOWER_CLASSES под вашу модель.'
        )

    model = build_model(len(FLOWER_CLASSES))
    model.load_state_dict(state_dict)
    model.eval()
    return model
