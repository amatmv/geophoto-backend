from django.urls import path
from .views import ListSearchAround, ListWithinAround, ListCreatePhotos, ListUsers


urlpatterns = [
    # Llistar usuaris
    path('users/', ListUsers.as_view(), name='users-list'),

    # Llistar fotos (sota condicions) i/o crear-les
    path('photos/', ListCreatePhotos.as_view(), name='photos-list-create'),

    # Llistar fotos al voltant d'un punt
    path('search_around/', ListSearchAround.as_view(), name="search-around"),

    # Llistar fotos dins una zona determinada
    path('search_within/', ListWithinAround.as_view(), name="search-within")

]

