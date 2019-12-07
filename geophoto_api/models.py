from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    full_name = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class Photo(models.Model):

    title = models.CharField(max_length=100)
    location = models.PointField(srid=25831)
    date_uploaded = models.DateField()
    widthPixels = models.PositiveIntegerField(null=True)
    heightPixels = models.PositiveIntegerField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Provincia(models.Model):

    name = models.CharField(max_length=100)
    codi = models.CharField(max_length=25)
    geom = models.MultiPolygonField(srid=25831)

