from typing import TypedDict

from langgraph.graph import END, StateGraph

from .predict import predict_flower


FLOWER_TRANSLATIONS = {
    'Ромашка': {'ru': 'Ромашка', 'en': 'Chamomile', 'latin': 'Matricaria chamomilla'},
    'Одуванчик': {'ru': 'Одуванчик', 'en': 'Dandelion', 'latin': 'Taraxacum officinale'},
    'Роза': {'ru': 'Роза', 'en': 'Rose', 'latin': 'Rosa'},
    'Подсолнух': {'ru': 'Подсолнух', 'en': 'Sunflower', 'latin': 'Helianthus annuus'},
    'Тюльпан': {'ru': 'Тюльпан', 'en': 'Tulip', 'latin': 'Tulipa'},
}

FLOWER_DESCRIPTIONS = {
    'Ромашка': 'Нежный полевой цветок с белыми лепестками и жёлтой сердцевиной; часто ассоциируется с лекарственными травами.',
    'Одуванчик': 'Яркий жёлтый цветок, который после цветения образует пушистый шарик из семян и легко распространяется ветром.',
    'Роза': 'Декоративный цветок с выразительным ароматом и множеством сортов, оттенков и форм бутона.',
    'Подсолнух': 'Крупный солнечный цветок с жёлтыми лепестками и большой сердцевиной, известный способностью поворачиваться к свету.',
    'Тюльпан': 'Весенний луковичный цветок с аккуратным бокаловидным бутоном и широкой палитрой цветов.',
}


class FlowerPipelineState(TypedDict, total=False):
    image: object
    predicted_class: str
    confidence: float
    names: dict[str, str]
    description: str
    confidence_status: str
    confidence_message: str


def identify_flower(state: FlowerPipelineState) -> FlowerPipelineState:
    predicted_class, confidence = predict_flower(state['image'])
    return {**state, 'predicted_class': predicted_class, 'confidence': confidence}


def translate_flower_name(state: FlowerPipelineState) -> FlowerPipelineState:
    predicted_class = state['predicted_class']
    names = FLOWER_TRANSLATIONS.get(
        predicted_class,
        {'ru': predicted_class, 'en': predicted_class, 'latin': 'Неизвестно'},
    )
    return {**state, 'names': names}


def add_flower_description(state: FlowerPipelineState) -> FlowerPipelineState:
    predicted_class = state['predicted_class']
    description = FLOWER_DESCRIPTIONS.get(
        predicted_class,
        'Описание для этого класса пока не добавлено.',
    )
    return {**state, 'description': description}


def check_model_confidence(state: FlowerPipelineState) -> FlowerPipelineState:
    confidence = state['confidence']
    if confidence >= 80:
        status = 'high'
        message = 'Высокая уверенность модели.'
    elif confidence >= 50:
        status = 'medium'
        message = 'Средняя уверенность: результат стоит проверить вручную.'
    else:
        status = 'low'
        message = 'Низкая уверенность: попробуйте загрузить более чёткое фото цветка.'

    return {**state, 'confidence_status': status, 'confidence_message': message}


def build_flower_pipeline():
    graph = StateGraph(FlowerPipelineState)
    graph.add_node('identify_flower', identify_flower)
    graph.add_node('translate_flower_name', translate_flower_name)
    graph.add_node('add_flower_description', add_flower_description)
    graph.add_node('check_model_confidence', check_model_confidence)

    graph.set_entry_point('identify_flower')
    graph.add_edge('identify_flower', 'translate_flower_name')
    graph.add_edge('translate_flower_name', 'add_flower_description')
    graph.add_edge('add_flower_description', 'check_model_confidence')
    graph.add_edge('check_model_confidence', END)
    return graph.compile()


_flower_pipeline = None


def get_flower_pipeline():
    global _flower_pipeline
    if _flower_pipeline is None:
        _flower_pipeline = build_flower_pipeline()
    return _flower_pipeline


def run_flower_pipeline(image_field_file) -> FlowerPipelineState:
    return get_flower_pipeline().invoke({'image': image_field_file})
