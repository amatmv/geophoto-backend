import boto3
import io
import base64

from PIL import Image
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import InMemoryUploadedFile

from rest_framework import generics, permissions
from rest_framework_jwt.settings import api_settings
from rest_framework.response import Response
from rest_framework.views import status

from geophoto.settings import AWS_S3_BASE_URL, AWS_STORAGE_BUCKET_NAME
from .decorators import validate_request_data_photo
from .serializers import PhotoSerializer, UserSerializer
from .models import *

User = get_user_model()

# Get the JWT settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class ListUsers(generics.ListCreateAPIView):
    """
    GET users/
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        try:
            users = self.queryset.filter(**kwargs)
            users_serialized = self.serializer_class(users, many=True).data
            return Response(users_serialized)
        except User.DoesNotExist:
            return Response(
                data={
                    "message": "User does not exist"
                },
                status=status.HTTP_404_NOT_FOUND
            )


class ListSearchAround(generics.ListCreateAPIView):
    """
    POST search_around/
    """
    serializer_class = PhotoSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        dist = request.data.get('distance')
        loc_lat = request.data.get('location_lat')
        loc_lon = request.data.get('location_lon')

        data = {}
        if loc_lon and loc_lon and dist:
            query = """
                SELECT 
                    uuid,
                    url, 
                    title, 
                    location AS point,
                    photo.user_id,
                    created_at,
                    prov.codiprov AS provincia,
                    mun.codimuni AS municipi,
                    comarca.codicomar AS comarca
                FROM geophoto_api_photo photo
                JOIN geophoto_api_provincia AS prov 
                    ON ST_Contains(prov.geom, photo.location) 
                JOIN geophoto_api_municipi AS mun
                    ON ST_Contains(mun.geom, photo.location)
                JOIN geophoto_api_comarca AS comarca
                    ON ST_Contains(comarca.geom, photo.location)
                WHERE ST_DWithin(
                    ST_Transform(photo.location, 4326)::geography, 
                    ST_SetSRID(ST_Makepoint({lon}, {lat}), 4326)::geography, 
                    {dist}
                )
                ORDER BY ST_Distance(
                    ST_SetSRID(ST_MakePoint({lon}, {lat}), 4326), 
                    ST_Transform(photo.location, 4326)
                );
            """.format(
                lon=loc_lon,
                lat=loc_lat,
                dist=dist
            )
            rows = Photo.objects.raw(raw_query=query)
            data = self.serializer_class(rows, many=True).data
        return Response(data)


class ListWithinAround(generics.ListCreateAPIView):
    """
    POST search_around/
    """
    serializer_class = PhotoSerializer
    permission_classes = (permissions.AllowAny,)

    def get_photos_taken_in_provincia(self, name):
        query = """
            SELECT
                uuid,
                url, 
                title, 
                location AS point,
                photo.user_id,
                created_at,
                prov.codiprov AS provincia,
                mun.codimuni AS municipi,
                comarca.codicomar AS comarca
            FROM geophoto_api_photo AS photo 
            JOIN geophoto_api_provincia AS prov 
                ON ST_Contains(prov.geom, photo.location) 
                AND prov.nomprov ILIKE '%%{prov_name}%%'
            JOIN geophoto_api_user u 
                ON u.id = photo.user_id
            JOIN geophoto_api_municipi AS mun
                ON ST_Contains(mun.geom, photo.location)
            JOIN geophoto_api_comarca AS comarca
                ON ST_Contains(comarca.geom, photo.location)
        """.format(prov_name=name)
        rows = Photo.objects.raw(raw_query=query)
        response_data = self.serializer_class(rows, many=True).data
        return response_data

    def get_photos_taken_in_comarca(self, name):
        query = """
            SELECT
                uuid,
                url, 
                title, 
                location AS point,
                photo.user_id,
                created_at,
                prov.codiprov AS provincia,
                mun.codimuni AS municipi,
                comarca.codicomar AS comarca
            FROM geophoto_api_photo AS photo 
            JOIN geophoto_api_provincia AS prov 
                ON ST_Contains(prov.geom, photo.location) 
            JOIN geophoto_api_user u 
                ON u.id = photo.user_id
            JOIN geophoto_api_municipi AS mun
                ON ST_Contains(mun.geom, photo.location)
            JOIN geophoto_api_comarca AS comarca
                ON ST_Contains(comarca.geom, photo.location)
                AND comarca.nomcomar ILIKE '%%{comarca_name}%%'
        """.format(comarca_name=name)
        rows = Photo.objects.raw(raw_query=query)
        response_data = self.serializer_class(rows, many=True).data
        return response_data

    def get_photos_taken_in_municipi(self, name):
        query = """
            SELECT
                uuid,
                url, 
                title, 
                location AS point,
                photo.user_id,
                created_at,
                prov.codiprov AS provincia,
                mun.codimuni AS municipi,
                comarca.codicomar AS comarca
            FROM geophoto_api_photo AS photo 
            JOIN geophoto_api_provincia AS prov 
                ON ST_Contains(prov.geom, photo.location) 
            JOIN geophoto_api_user u 
                ON u.id = photo.user_id
            JOIN geophoto_api_municipi AS mun
                ON ST_Contains(mun.geom, photo.location)
                AND mun.nommuni ILIKE '%%{mun_name}%%'
            JOIN geophoto_api_comarca AS comarca
                ON ST_Contains(comarca.geom, photo.location)
        """.format(mun_name=name)
        rows = Photo.objects.raw(raw_query=query)
        response_data = self.serializer_class(rows, many=True).data
        return response_data

    def post(self, request, *args, **kwargs):
        zone = request.data.get('zone')
        zone_type = request.data.get('zone_type', '')

        response_data = {}
        if zone_type not in ('provincia', 'comarca', 'municipi'):
            response_status = status.HTTP_400_BAD_REQUEST
        else:
            # try:
            if zone_type == 'provincia':
                response_data = self.get_photos_taken_in_provincia(zone)
            elif zone_type == 'comarca':
                response_data = self.get_photos_taken_in_comarca(zone)
            elif zone_type == 'municipi':
                response_data = self.get_photos_taken_in_municipi(zone)

            response_status = status.HTTP_200_OK
            # except Exception as e:
            #     response_status = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(data=response_data, status=response_status)


class ListCreatePhotos(generics.ListCreateAPIView):
    """
    GET photo/
    POST photo/
    """
    queryset = Photo.objects.all().order_by('-date_uploaded')
    serializer_class = PhotoSerializer

    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def get_bytesIO(data):
        if isinstance(data, InMemoryUploadedFile):
            photo_buf = io.BytesIO(data.file.getvalue())
        else:
            b64_decoded = base64.b64decode(data)
            photo_buf = io.BytesIO(b64_decoded)
        return photo_buf

    @staticmethod
    def upload_s3_photo(photo_binary, key=None):
        s3 = boto3.client('s3')

        if key is None:
            key = uuid.uuid4().hex[:6] + '.jpg'

        s3.upload_fileobj(photo_binary, AWS_STORAGE_BUCKET_NAME, key)
        url = "{aws_s3_url}{bucket_name}/{key}".format(
            aws_s3_url=AWS_S3_BASE_URL,
            bucket_name=AWS_STORAGE_BUCKET_NAME,
            key=key
        )
        return url

    @staticmethod
    def generate_photo_name(photo_name):
        return photo_name[:6] + '.jpg'

    @validate_request_data_photo
    def post(self, request, *args, **kwargs):
        date_uploaded = datetime.today().strftime('%Y-%m-%d')

        photo_file = request.data['photo']
        bytes_data = self.get_bytesIO(photo_file)
        exif_data = Photo.extract_exif_data(Image.open(bytes_data))

        created_photo = None
        try:
            create_vals = {
                'title': request.data["title"],
                'date_uploaded': date_uploaded,
                'user': request.user,
            }
            create_vals.update(exif_data)

            created_photo = Photo.objects.create(**create_vals)

            respose_data = {
                'message': 'Photo posted successfully!'
            }
            response_status = status.HTTP_201_CREATED
        except Exception as e:
            respose_data = {
                "message": "Internal server error."
            }
            response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
            print(e)

        if created_photo is not None:
            bytes_data = self.get_bytesIO(photo_file)
            key = self.generate_photo_name(created_photo.uuid.hex)
            url = self.upload_s3_photo(bytes_data, key=key)
            created_photo.url = url
            created_photo.save()

        return Response(
            data=respose_data,
            status=response_status
        )

    def get(self, request, *args, **kwargs):
        try:
            photos = self.queryset.get(kwargs=kwargs)
            return Response(self.serializer_class(photos).data)
        except Photo.DoesNotExist:
            return Response(
                data={
                    "message": "Photo does not exist"
                },
                status=status.HTTP_404_NOT_FOUND
            )


class RegisterUsers(generics.CreateAPIView):
    """
    POST auth/register/
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        email = request.data.get("email", "")
        if not username and not password and not email:
            return Response(
                data={
                    "message": "username, password and email is required to register a user"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        full_name = request.data.get('full_name', '')
        new_user = User.objects.create_user(
            username=username, password=password, email=email, full_name=full_name
        )
        return Response(
            data=UserSerializer(new_user).data,
            status=status.HTTP_201_CREATED
        )
