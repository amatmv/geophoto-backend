# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.gis.db import models


class Photo(models.Model):

    title = models.CharField(max_length=100)
    location = models.PointField()
    widthPixels = models.PositiveIntegerField()
    heightPixels = models.PositiveIntegerField()

