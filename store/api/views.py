from rest_framework.decorators import  api_view, action
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import StoreSerializer
from login.models import User,Store

class Storeviewset(viewsets.ModelViewset):
    serializer_class = StoreSerializer
    queryset = Store.objects.all()
    
    @action(method = ['POST'],detail=False, url_path ="store" , url_name="post_store")
    def post_store(self,request, *args, **kwargs ):
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        birthday = request.POST.get('birthday')