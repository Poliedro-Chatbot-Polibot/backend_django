from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'register', views.UserRegisterViewSet, basename='user-register')


urlpatterns = [
    path('', include(router.urls)),
    path('', include('dj_rest_auth.urls')),
]