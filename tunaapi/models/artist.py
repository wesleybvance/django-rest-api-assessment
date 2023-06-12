from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=50)
    bio = models.CharField(max_length=50)
    age = models.IntegerField()

    @property
    def songs(self):
        return self.__songs

    @songs.setter
    def songs(self, value):
        self.__songs = value
