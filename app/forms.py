from django import forms

from .models import UploadedFlowerImage


class FlowerUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFlowerImage
        fields = ['image']
        labels = {'image': 'Выберите изображение цветка'}
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }
