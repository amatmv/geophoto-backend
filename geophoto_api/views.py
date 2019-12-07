from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate, login

from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import status

from .decorators import validate_request_data
from .serializers import PhotoSerializer, UserSerializer, TokenSerializer
from .models import Photo
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()

# Get the JWT settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class ListCreateUsers(generics.ListCreateAPIView):
    """
    GET photo/
    POST photo/
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            users = self.queryset.get()
            return Response(self.serializer_class(users).data)
        except User.DoesNotExist:
            return Response(
                data={
                    "message": "User does not exist"
                },
                status=status.HTTP_404_NOT_FOUND
            )


class ListCreatePhotos(generics.ListCreateAPIView):
    """
    GET photo/
    POST photo/
    """
    queryset = Photo.objects.all().order_by('-date_uploaded')
    serializer_class = PhotoSerializer

    permission_classes = (permissions.IsAuthenticated,)

    @validate_request_data
    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=kwargs['user_id'])
        a_song = Photo.objects.create(
            title=request.data["title"], user=user
        )
        return Response(
            data=PhotoSerializer(a_song).data,
            status=status.HTTP_201_CREATED
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


class LoginView(generics.CreateAPIView):
    """
    POST auth/login/
    """

    # This permission class will over ride the global permission
    # class setting
    permission_classes = (permissions.AllowAny,)

    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # login saves the user’s ID in the session,
            # using Django’s session framework.
            login(request, user)
            serializer = TokenSerializer(data={
                # using drf jwt utility functions to generate a token
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


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
