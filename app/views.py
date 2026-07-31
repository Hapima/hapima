from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db import OperationalError
from django.shortcuts import redirect, render

from .forms import FlowerUploadForm


def signup(request):
    if request.user.is_authenticated:
        return redirect('upload_image')

    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('upload_image')

    return render(request, 'registration/signup.html', {'form': form})


@login_required
def upload_image(request):
    prediction = None
    form = FlowerUploadForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        from ml.flower_pipeline import run_flower_pipeline

        uploaded_obj = form.save(commit=False)
        try:
            pipeline_result = run_flower_pipeline(uploaded_obj.image)
            names = pipeline_result.get('names', {})
            uploaded_obj.predicted_class = pipeline_result['predicted_class']
            uploaded_obj.confidence = pipeline_result['confidence']
            uploaded_obj.name_ru = names.get('ru', uploaded_obj.predicted_class)
            uploaded_obj.name_en = names.get('en', '')
            uploaded_obj.name_latin = names.get('latin', '')
            uploaded_obj.description = pipeline_result.get('description', '')
            uploaded_obj.confidence_status = pipeline_result.get('confidence_status', '')
            uploaded_obj.confidence_message = pipeline_result.get('confidence_message', '')
            uploaded_obj.save()
            prediction = uploaded_obj
        except OperationalError:
            form.add_error(
                None,
                'База данных не инициализирована. Выполните: '
                '`python manage.py makemigrations` и `python manage.py migrate`, затем перезапустите сервер.',
            )
        except Exception as exc:
            form.add_error(None, f'Ошибка инференса: {exc}')

    return render(
        request,
        'app/upload.html',
        {
            'form': form,
            'prediction': prediction,
        },
    )
