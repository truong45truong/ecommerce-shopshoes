from rest_framework.serializers import ModelSerializer,Serializer
from login.models import User,Customer
from rest_framework import serializers
import datetime
class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
    def create(self, validated_data):
        size =Customer.objects.create( **validated_data)
        return size
    
class UserSerializer(Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
    style={'input_type': 'password'})
    name = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField()
    customer_id = CustomerSerializer(many = False)
    class Meta:
        model = User
        fields = ['username','password','name','email','phone','customer_id']
