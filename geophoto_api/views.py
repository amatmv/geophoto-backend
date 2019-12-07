from django.shortcuts import render

from .models import *
from .serializers import *


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all().order_by('-date_uploaded')
    serializer_class = PhotoSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

