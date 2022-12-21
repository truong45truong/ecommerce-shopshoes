from rest_framework.serializers import ModelSerializer,Serializer
from login.models import User
from rest_framework import serializers
import datetime
class UserSerializer(Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
    style={'input_type': 'password'})
    name = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField()
