import torch
from PIL import Image

from .model import load_trained_model

_processor = None
_model = None


def _get_model():
    global _processor, _model
    if _model is None:
        _processor, _model = load_trained_model()
    return _processor, _model


def predict_flower(image_field_file):
    processor, model = _get_model()

    image_field_file.seek(0)
    image = Image.open(image_field_file).convert('RGB')
    inputs = processor(images=image, return_tensors='pt')

    with torch.inference_mode():
        logits = model(**inputs).logits
        probabilities = torch.softmax(logits, dim=-1)[0]
        confidence, class_idx = torch.max(probabilities, dim=0)

    label_id = class_idx.item()
    class_name = model.config.id2label.get(label_id, str(label_id))
    return class_name, float(confidence.item() * 100)
