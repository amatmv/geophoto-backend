from django.urls import path
from .views import ListSearchAround, ListWithinAround, ListCreatePhotos, ListUsers, ListUserPhotos


urlpatterns = [
    # Llistar usuaris
    path('users/', ListUsers.as_view(), name='users-list'),

    # Llistar fotos (sota condicions) i/o crear-les
    path('photos/', ListCreatePhotos.as_view(), name='photos-list-create'),

    # Llistar fotos al voltant d'un punt
    path('search_around/', ListSearchAround.as_view(), name="search-around"),

    # Llistar fotos dins una zona determinada
    path('search_within/', ListWithinAround.as_view(), name="search-within"),

    # Llistar fotos d'un usuari en concret
    path('search_my_photos/', ListUserPhotos.as_view(), name="search-my-photos")
]

