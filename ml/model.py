import os

from transformers import AutoImageProcessor, AutoModelForImageClassification


# The repository contains a ViT-B/16 model fine-tuned on all 102 Oxford Flowers
# classes. Override this value to use a local snapshot in an offline deployment.
MODEL_ID = os.getenv('FLOWER_MODEL_ID', 'oschamp/vit-base-oxford-flowers-102')


def load_trained_model(model_id: str = MODEL_ID):
    """Load the Hugging Face processor and fine-tuned ViT classifier."""
    try:
        processor = AutoImageProcessor.from_pretrained(model_id)
        model = AutoModelForImageClassification.from_pretrained(
            model_id,
            use_safetensors=True,
        )
    except OSError as exc:
        raise RuntimeError(
            f'Не удалось загрузить модель {model_id!r} из Hugging Face. '
            'Проверьте подключение к интернету или задайте FLOWER_MODEL_ID '
            'как путь к локально сохранённой модели.'
        ) from exc

    model.eval()
    return processor, model
