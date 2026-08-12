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
│   └── predict.py
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

## Модель классификации

Приложение использует готовую модель Hugging Face
[`oschamp/vit-base-oxford-flowers-102`](https://huggingface.co/oschamp/vit-base-oxford-flowers-102):
ViT Base, дообученный на 102 классах Oxford Flowers. При первом запросе
`transformers` автоматически скачает конфигурацию, image processor и веса
`model.safetensors`, а затем будет использовать локальный кеш Hugging Face.

Для офлайн-запуска заранее скачайте snapshot модели и задайте путь к нему:

```bash
export FLOWER_MODEL_ID=/path/to/vit-base-oxford-flowers-102
```

В каталоге должны находиться файлы Hugging Face-модели, включая
`config.json`, конфигурацию processor и `model.safetensors`.

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

## Авторизация

- Теперь загрузка изображения доступна только авторизованным пользователям.
- Регистрация: `http://127.0.0.1:8000/signup/`
- Вход: `http://127.0.0.1:8000/accounts/login/`
- Выход доступен кнопкой в верхней панели интерфейса.

## Поток работы

1. На главной странице загрузите картинку.
2. Нажмите «Готово».
3. Django передаст изображение в LangGraph-пайплайн из `ml/flower_pipeline.py`.
4. Первый узел запускает ViT-модель из Hugging Face и определяет один из 102 классов цветков.
5. Второй узел добавляет названия на русском, английском и латыни.
6. Третий узел добавляет краткое описание цветка.
7. Четвёртый узел проверяет уверенность модели и формирует подсказку для пользователя.
8. Django сохраняет файл и результат в `media/uploads/`, после чего показывает расширенный ответ на странице.


## Ошибка загрузки модели

Если Hugging Face недоступен при первом запуске, приложение покажет понятную
ошибку. Подключитесь к интернету для заполнения кеша либо скачайте модель
заранее и укажите локальный каталог через `FLOWER_MODEL_ID`.



## Частая ошибка: `no such table: app_uploadedflowerimage`

Это означает, что миграции не были применены к базе данных SQLite.

Выполните в терминале из корня проекта:

```bash
python manage.py makemigrations
python manage.py migrate
```

После этого перезапустите сервер:

```bash
python manage.py runserver
```
