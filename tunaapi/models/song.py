from django.db import models
from .artist import Artist

class Song(models.Model):
    title = models.CharField(max_length=200)
    album = models.CharField(max_length=55)
    length = models.DecimalField(max_length=4,decimal_places=2)
    artist_id = models.ForeignKey(Artist, on_delete=models.CASCADE)
