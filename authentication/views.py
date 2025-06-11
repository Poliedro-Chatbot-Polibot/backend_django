from django.contrib.auth.models import Group
from rest_framework import permissions, viewsets




from . import models
from .serializers import GroupSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserRegisterViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = UserSerializer
    permission_classes = ([])
    http_method_names = ['post']

    


    