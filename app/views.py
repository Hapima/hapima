from django.shortcuts import render

from .forms import FlowerUploadForm


def upload_image(request):
    prediction = None
    form = FlowerUploadForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        from ml.predict import predict_flower

        uploaded_obj = form.save(commit=False)
        predicted_class, confidence = predict_flower(uploaded_obj.image)
        uploaded_obj.predicted_class = predicted_class
        uploaded_obj.confidence = confidence
        uploaded_obj.save()
        prediction = uploaded_obj

    return render(
        request,
        'app/upload.html',
        {
            'form': form,
            'prediction': prediction,
        },
    )
