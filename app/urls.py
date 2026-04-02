from django.urls import path

from .views import signup, upload_image

urlpatterns = [
    path('', upload_image, name='upload_image'),
    path('signup/', signup, name='signup'),
]
