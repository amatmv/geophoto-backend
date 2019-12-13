from django.urls import path
from .views import ListSearchAround, RegisterUsers, ListCreatePhotos, ListUsers


urlpatterns = [
    # Llistar usuaris
    path('users/', ListUsers.as_view(), name='users-list'),

    # Llistar fotos (sota condicions) i/o crear-les
    path('photos/', ListCreatePhotos.as_view(), name='photos-list-create'),

    # Autenticació d'usuaris
    path('register/', RegisterUsers.as_view(), name="auth-register"),

    # Llistar fotos al voltant d'un punt
    path('search_around/', ListSearchAround.as_view(), name="search-around")
]
