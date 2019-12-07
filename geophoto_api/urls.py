from django.urls import path
from .views import LoginView, RegisterUsers, ListCreatePhotos


urlpatterns = [
    # path('users', ListCreateUsers.as_view(), name='list_users'),
    path('photos', ListCreatePhotos.as_view(), name='photos-list-create'),
    path('auth/login/', LoginView.as_view(), name="auth-login"),
    path('auth/register/', RegisterUsers.as_view(), name="auth-register")
]