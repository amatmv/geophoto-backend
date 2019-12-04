from tastypie.resources import ModelResource
from geophoto_api.models import Photo


class PhotoResource(ModelResource):
    class Meta:
        queryset = Photo.objects.all()
        resource_name = 'photo'