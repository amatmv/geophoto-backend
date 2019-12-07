# coding=utf-8
from geophoto_api.models import *
from rest_framework import serializers


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('id', 'title', 'location')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('username', 'full_name')
