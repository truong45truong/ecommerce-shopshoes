from rest_framework.decorators import  api_view, action
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import StoreSerializer
from login.models import User,Store
import json

class Storeviewset(viewsets.ModelViewSet):
    serializer_class = StoreSerializer
    queryset = Store.objects.all()
    
    @action(method = ['POST'],detail=False, url_path ="store" , url_name="post_store")
    def post_store(self,request, *args, **kwargs ):
        emailUser = request.POST.get('email-user')
        
        name = request.POST.get('name')
        email = request.POST.get('email')
        city = request.POST.get('city')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        contact = request.POST.get('contact')
        fax = request.POST.get('fax')
        
        print(email)
        userStore = User.objects.filter(email=emailUser)
        if(userStore):
            store = Store.objects.create(name=name,contact=contact,address=address,city=city,phone=phone,fax=fax)
            userStore.store_id = store
            userStore.save()
        else :
            return Response(False)
        return Response('Register store success')
        
    @action(method = ['GET'],detail=False, url_path ="store" , url_name="get_store")
    def get_store(self,request, *args, **kwargs):
        emailStore = request.GET.get('email-store')
        emailUser = request.GET.get('email-user')
        queryset = Store.objects.filter(email=emailStore,users__email=emailUser)
        serializer = StoreSerializer(queryset,many=True)
        
        return Response(serializer.data)
    @action (method = ['PUT'],detail=False, url_path ="store" , url_name="put_store")
    def put_store(self,request, *args, **kwargs):
        emailStore = request.GET.get('email-store')
        data =request.POST
        try : 
            store = Store.objects.get(email=emailStore)
            store.name= data['name']
            store.contact = data['contact']
            store.city = data['city']
            store.phone = data['phone']
            store.address = data['address']
            store.fax = data['fax']
            store.email = data['email']
            store.save()
        except:
            return Response(False)
        
        return Response('Update store success')