from django.urls import path
from .views import LoginView, RegisterUsers, ListCreatePhotos, ListCreateUsers


urlpatterns = [
    # Llistar usuaris
    path('users/', ListCreateUsers.as_view(), name='users-list'),

    # Llistar fotos (sota condicions) i/o crear-les
    path('photos/', ListCreatePhotos.as_view(), name='photos-list-create'),

    # Autenticació d'usuaris
    path('login/', LoginView.as_view(), name="auth-login"),
    path('register/', RegisterUsers.as_view(), name="auth-register")
]
