from django.db import models

# Create your models here.
class Song(models.Model):
    audio_file = models.FileField(upload_to='media/', null=True, blank=True)