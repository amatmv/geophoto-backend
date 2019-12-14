# coding=utf-8
from .models import Photo
from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class PhotoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('title', 'location', 'date_uploaded', 'widthPixels', 'heightPixels', 'user_id', 'created_at', 'photo',
                  'uuid')


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('title', 'location', 'date_uploaded')


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "full_name")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "full_name")


class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)
