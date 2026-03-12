from django.db import models


class UploadedFlowerImage(models.Model):
    image = models.ImageField(upload_to='uploads/')
    predicted_class = models.CharField(max_length=100, blank=True)
    confidence = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.predicted_class or 'Unknown'} ({self.created_at:%Y-%m-%d %H:%M})"
