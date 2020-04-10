from django.db import models


class ImageModel(models.Model):
    """модель загрузки изображений"""
    hash = models.TextField(primary_key=True)
    img = models.ImageField(upload_to='img/')
    date = models.DateTimeField(auto_now_add=True)
