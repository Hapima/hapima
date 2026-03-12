from django.contrib import admin

from .models import UploadedFlowerImage


@admin.register(UploadedFlowerImage)
class UploadedFlowerImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'predicted_class', 'confidence', 'created_at')
    readonly_fields = ('created_at',)
