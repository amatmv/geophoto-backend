from django.contrib.gis.db import models
from django.contrib.auth.models import User


class User(models.Model):

    username = models.CharField(max_length=20)
    full_name = models.CharField(max_length=64)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.full_name


class Photo(models.Model):

    title = models.CharField(max_length=100)
    location = models.PointField(srid=25831)
    date_uploaded = models.DateField()
    widthPixels = models.PositiveIntegerField(null=True)
    heightPixels = models.PositiveIntegerField(null=True)


class Provincia(models.Model):

    name = models.CharField(max_length=100)
    codi = models.CharField(max_length=25)
    geom = models.MultiPolygonField(srid=25831)

