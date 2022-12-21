from rest_framework.serializers import ModelSerializer,Serializer
from login.models import User
from rest_framework import serializers
import datetime
class UserSerializer(Serializer):
    username = serializers.CharField(source="user.username")
    password = serializers.CharField( source="user.password",
    style={'input_type': 'password'})
    name = serializers.CharField(source="user.name")
    email = serializers.EmailField(source="user.email")
    phone = serializers.CharField(source="user.phone")
    address = serializers.CharField(source="user.address")
    birthday = serializers.DateField(initial=datetime.date.today,source="user.birthday")
