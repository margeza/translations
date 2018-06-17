from django.db import models
from django.utils import timezone


class Translation(models.Model):
    key = models.CharField(max_length=200)
    english_translation = models.TextField()
    spanish_translation = models.TextField()
    status = models.BooleanField()

    def __str__(self):
        return self.key