from django.db import models

# Create your models here.
# myapp/models.py
from django.db import models

class Track(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    genre = models.CharField(max_length=50, default='Unknown')  # デフォルト値を指定)
    release_date = models.DateField()

    def __str__(self):
        return self.title
