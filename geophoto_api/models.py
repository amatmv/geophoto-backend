from PIL import Image
from six import StringIO
from PIL.ExifTags import TAGS, GPSTAGS
from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    full_name = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class Photo(models.Model):

    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False,
    )
    photo = models.ImageField(default='default.jpg', null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    title = models.CharField(max_length=100)
    location = models.PointField(srid=25831)
    date_uploaded = models.DateField()
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
                lat = str(f"{lat:.{5}f}")
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
                lon = str(f"{lon:.{5}f}")
                return lon
        else:
            return None

    @staticmethod
    def get_date_time(exifdata):
        if 'DateTime' in exifdata:
            date_and_time = exifdata['DateTime']
            return date_and_time

    @staticmethod
    def extract_exif_data(binary_photo):
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

        image = Image.open(StringIO(binary_photo))
        exifdata = get_exif_data(image)

        lat = Photo.get_lat(exifdata)
        lon = Photo.get_lon(exifdata)

        location = "POINT({lat} {long})".format(lat=lat, long=lon)
        width = exifdata['YResolution']
        height = exifdata['XResolution']

        date_taken = Photo.get_date_time(exifdata)
        res = {
            'location': location,
            'widthPixels': width,
            'heightPixels': height,
            'date_taken': date_taken
        }
        return res


class Provincia(models.Model):

    name = models.CharField(max_length=100)
    codi = models.CharField(max_length=25)
    geom = models.MultiPolygonField(srid=25831)

