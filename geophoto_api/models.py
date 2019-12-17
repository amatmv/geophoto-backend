from PIL import Image
from io import BytesIO
from datetime import datetime
from PIL.ExifTags import TAGS, GPSTAGS
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.auth.models import AbstractUser
from django.contrib.gis.gdal import SpatialReference, CoordTransform

import uuid


class User(AbstractUser):
    full_name = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class Photo(models.Model):

    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False,
    )
    url = models.CharField(max_length=200, default='foo.com')
    created_at = models.DateTimeField()

    title = models.CharField(max_length=100)
    location = models.PointField(srid=25831)
    date_uploaded = models.DateTimeField()
    widthPixels = models.PositiveIntegerField(null=True)
    heightPixels = models.PositiveIntegerField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @staticmethod
    def get_if_exist(data, key):
        if key in data:
            return data[key]
        return None

    @staticmethod
    def convert_to_degress(value):
        """Helper function to convert the GPS coordinates
        stored in the EXIF to degress in float format"""
        d0 = value[0][0]
        d1 = value[0][1]
        d = float(d0) / float(d1)
        m0 = value[1][0]
        m1 = value[1][1]
        m = float(m0) / float(m1)

        s0 = value[2][0]
        s1 = value[2][1]
        s = float(s0) / float(s1)

        return d + (m / 60.0) + (s / 3600.0)

    @staticmethod
    def get_lat(exifdata):
        """Returns the latitude and longitude, if available, from the
        provided exif_data (obtained through get_exif_data above)"""
        # print(exif_data)
        if 'GPSInfo' in exifdata:
            gps_info = exifdata["GPSInfo"]
            gps_latitude = Photo.get_if_exist(gps_info, "GPSLatitude")
            gps_latitude_ref = Photo.get_if_exist(gps_info, 'GPSLatitudeRef')
            if gps_latitude and gps_latitude_ref:
                lat = Photo.convert_to_degress(gps_latitude)
                if gps_latitude_ref != "N":
                    lat = 0 - lat
                lat = str("{0:.5f}".format(lat))
                return lat
        else:
            return None

    @staticmethod
    def get_lon(exifdata):
        """Returns the latitude and longitude, if available, from the
        provided exif_data (obtained through get_exif_data above)"""
        # print(exif_data)
        if 'GPSInfo' in exifdata:
            gps_info = exifdata["GPSInfo"]
            gps_longitude = Photo.get_if_exist(gps_info, 'GPSLongitude')
            gps_longitude_ref = Photo.get_if_exist(gps_info, 'GPSLongitudeRef')
            if gps_longitude and gps_longitude_ref:
                lon = Photo.convert_to_degress(gps_longitude)
                if gps_longitude_ref != "E":
                    lon = 0 - lon
                lon = str("{0:.5f}".format(lon))
                return lon
        else:
            return None

    @staticmethod
    def get_date_time(exifdata):
        if 'DateTime' in exifdata:
            date_and_time = exifdata['DateTime']
            date_and_time = datetime.strptime(
                date_and_time, '%Y:%m:%d %H:%M:%S'
            ).strftime('%Y-%m-%d %H:%M:%S')
            return date_and_time

    @staticmethod
    def extract_exif_data(image):
        exifdata = Photo.get_exif_data(image)

        lat = Photo.get_lat(exifdata)
        lon = Photo.get_lon(exifdata)

        width, height = image.size

        date_taken = Photo.get_date_time(exifdata)
        pnt = False
        if lat and lon:
            transform = CoordTransform(SpatialReference(4326), SpatialReference(25831))
            pnt = Point(float(lon), float(lat))
            pnt.transform(transform)

        res = {
            'location': pnt,
            'widthPixels': width,
            'heightPixels': height,
            'created_at': date_taken
        }
        return res

    @staticmethod
    def get_exif_data(image):
        """Returns a dictionary from the exif data of an PIL Image item. Also
        converts the GPS Tags"""
        exif_data = {}
        info = image._getexif()
        if info:
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                if decoded == "GPSInfo":
                    gps_data = {}
                    for t in value:
                        sub_decoded = GPSTAGS.get(t, t)
                        gps_data[sub_decoded] = value[t]

                    exif_data[decoded] = gps_data
                else:
                    exif_data[decoded] = value
        return exif_data


class Provincia(models.Model):

    nomprov = models.CharField(max_length=100)
    codiprov = models.CharField(max_length=25)
    areaprov = models.FloatField(null=True)
    geom = models.MultiPolygonField(srid=25831)

    class Meta:
        ordering = ('nomprov',)
        verbose_name_plural = ('provincies',)


class Comarca(models.Model):

    nomcomar = models.CharField(max_length=100)
    codicomar = models.CharField(max_length=25)
    areacomar = models.FloatField(null=True)
    geom = models.MultiPolygonField(srid=25831)

    class Meta:
        ordering = ('nomcomar',)
        verbose_name_plural = ('comarques',)


class Municipi(models.Model):

    nommuni = models.CharField(max_length=100)
    codimuni = models.CharField(max_length=25)
    codicomar = models.CharField(max_length=25)
    codiprov = models.CharField(max_length=25)
    comarca = models.ForeignKey(Comarca, on_delete=models.CASCADE, null=True)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE, null=True)
    areapol = models.FloatField(null=True)
    geom = models.MultiPolygonField(srid=25831)

    class Meta:
        ordering = ('nommuni',)
        verbose_name_plural = ('municipis',)
