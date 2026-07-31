from django.db import models


class UploadedFlowerImage(models.Model):
    image = models.ImageField(upload_to='uploads/')
    predicted_class = models.CharField(max_length=100, blank=True)
    confidence = models.FloatField(null=True, blank=True)
    name_ru = models.CharField(max_length=100, blank=True)
    name_en = models.CharField(max_length=100, blank=True)
    name_latin = models.CharField(max_length=150, blank=True)
    description = models.TextField(blank=True)
    confidence_status = models.CharField(max_length=20, blank=True)
    confidence_message = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.predicted_class or 'Unknown'} ({self.created_at:%Y-%m-%d %H:%M})"
