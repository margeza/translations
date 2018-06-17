from django.db import models

class Translation(models.Model):
    key = models.CharField(max_length=200)
    english_translation = models.TextField()
    spanish_translation = models.TextField()
    DONE = "Y"
    TODO = "N"
    SIMILAR = "S"
    STATUS_CHOICES = (
        (DONE, 'Yes'),
        (TODO, 'No'),
        (SIMILAR, 'Similar')
    )
    status = models.CharField(verbose_name="Corrected", max_length=1, choices=STATUS_CHOICES, default="N")

    def __str__(self):
        return self.key