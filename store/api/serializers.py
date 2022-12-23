from rest_framework import serializers


class StoreSerializer (serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField()
    address = serializers.CharField()
    city = serializers.CharField()
    fax = serializers.CharField()
    contact = serializers.CharField()
    