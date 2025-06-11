from django.contrib.auth.models import Group
from rest_framework import serializers
from dj_rest_auth.serializers import UserDetailsSerializer


from . import models


from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk','url', 'username', 'email', 'groups', 'password','first_name','last_name']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True, 'style': {'input_type': 'password'}},
            'groups': {'required': False},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        return user

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + \
            ('is_staff', 'is_superuser',)
        extra_kwargs = {
            'is_staff': {'read_only': True},
            'is_superuser': {'read_only': True},
            'email': {'read_only': False},
        }
