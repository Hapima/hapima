# Flower Classifier Django (MVP)

## Структура

```text
hapima/
├── app/
│   ├── templates/app/upload.html
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── ml/
│   ├── model.py
│   ├── predict.py
│   └── flower_model.pth   <- сюда положить веса
├── project/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── static/css/styles.css
├── templates/base.html
├── media/
├── manage.py
└── requirements.txt
```

## Куда класть обученную модель

Положите файл весов в путь:

```text
ml/flower_model.pth
```

Если путь отличается, поменяйте константу `MODEL_WEIGHTS_PATH` в `ml/model.py`.

## Запуск в PyCharm

1. Откройте папку проекта в PyCharm.
2. Создайте виртуальное окружение Python 3.10+.
3. Установите зависимости:

```bash
pip install -r requirements.txt
```

4. Выполните миграции:

```bash
python manage.py makemigrations
python manage.py migrate
```

5. Запустите сервер:

```bash
python manage.py runserver
```

6. Откройте `http://127.0.0.1:8000/` и загрузите изображение цветка.

## Поток работы

1. На главной странице загрузите картинку.
2. Нажмите «Готово».
3. Django сохранит файл в `media/uploads/`.
4. Модель из `ml/flower_model.pth` выполнит инференс.
5. Результат и вероятность покажутся на той же странице.
