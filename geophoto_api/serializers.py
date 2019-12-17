# coding=utf-8
from .models import *
from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "full_name")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", )


class PhotoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('title', 'location', 'date_uploaded', 'widthPixels', 'heightPixels', 'user_id', 'created_at', 'photo',
                  'uuid')


class ProvinciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provincia
        fields = ('nomprov',)


class PhotoSerializer(serializers.ModelSerializer):

    user = UserSerializer()
    provincia = serializers.SerializerMethodField()
    comarca = serializers.SerializerMethodField()
    municipi = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ('title', 'location', 'created_at', 'user', 'url', 'provincia', 'comarca', 'municipi')

    def get_created_at(self, obj):
        return obj.created_at.strftime('%a %d, %b %Y at %H:%M')

    def get_provincia(self, obj):
        provincia = Provincia.objects.filter(codiprov=obj.provincia)
        nomprov = 'Província desconeguda'
        if provincia:
            nomprov = provincia[0].nomprov
        return nomprov

    def get_municipi(self, obj):
        municipi = Municipi.objects.filter(codimuni=obj.municipi)
        nommuni = 'Municipi desconegut'
        if municipi:
            nommuni = municipi[0].nommuni
        return nommuni

    def get_comarca(self, obj):
        comarca = Comarca.objects.filter(codicomar=obj.comarca)
        nomcomar = 'Comarca desconeguda'
        if comarca:
            nomcomar = comarca[0].nomcomar
        return nomcomar


class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)
