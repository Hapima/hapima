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


## Где взять `ml/flower_model.pth`

Есть 3 рабочих варианта:

1. **Взять готовые веса из вашего обучения** (самый правильный путь).
   - Если вы обучали модель в Jupyter/Colab, сохраните state dict:

```python
torch.save(model.state_dict(), "flower_model.pth")
```

   - Скопируйте файл в проект: `ml/flower_model.pth`.

2. **Скачать готовые веса из вашего репозитория/облака**.
   - Часто веса хранят в Releases GitHub, Google Drive, Яндекс.Диск или S3.
   - После скачивания просто переименуйте файл в `flower_model.pth` и положите в папку `ml/`.

3. **Быстро дообучить на датасете Flowers-5/Flowers-102 и сохранить веса**.
   - Важно: архитектура при обучении должна совпадать с `ml/model.py` (ResNet18 + ваш `num_classes`).
   - После обучения сохраните только `state_dict` в `ml/flower_model.pth`.

### Проверка совместимости весов

Веса должны быть сохранены как `state_dict` для модели ResNet18 с такой же последней `fc`-головой (число классов = длина `FLOWER_CLASSES`).
Если классов другое количество, обновите список `FLOWER_CLASSES` и переобучите/пересохраните веса.

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


## Частая ошибка: size mismatch для `fc.weight` / `fc.bias`

Если видите ошибку вида:

```
size mismatch for fc.weight: ... [1000, 512] ... expected [5, 512]
```

значит вы подложили веса от ImageNet-модели (1000 классов) или от модели с другим числом классов.

Что делать:

1. Использовать веса именно вашей обученной flower-модели, где число классов совпадает с `FLOWER_CLASSES`.
2. Либо привести `FLOWER_CLASSES` к реальному числу классов модели и переобучить/пересохранить чекпойнт.
3. Убедиться, что сохраняете `state_dict` после замены финального слоя на нужное число классов.

Теперь приложение покажет понятную ошибку на странице вместо падения Django.

