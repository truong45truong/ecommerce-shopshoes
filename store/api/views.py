from rest_framework.decorators import  api_view, action
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import StoreSerializer
from login.models import User,Store

class Storeviewset(viewsets.ModelViewSet):
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
        
    @action(method = ['GET'],detail=False, url_path ="store" , url_name="get_store")
    def get_store(self,request, *args, **kwargs):
        emailStore = request.GET.get('email-store')
        emailUser = request.GET.get('email-user')
        print(emailStore)
        queryset = Store.objects.filter(email=emailStore,users__email=emailUser)
        serializer = StoreSerializer(queryset,many=True)
        
        return Response(serializer.data)
    @action (method = ['PUT'],detail=False, url_path ="store" , url_name="put_store")
    def put_store(self,request, *args, **kwargs):
        dataPut = request.PUT.get('data')
        return Response(dataPut)