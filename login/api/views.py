from rest_framework.decorators import  api_view, action
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import UserSerializer
from login.models import User,Customer


class Userviewset(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
    @action(methods=['GET'],detail=False , url_path="user",url_name="get_user")
    def get_user(self,request,*args, **kwargs):
        username = request.GET.get('username')
        password = request.GET.get('password')
        queryset = User.objects.filter(username=username)
        if queryset[0].check_password(password):
            serializer = UserSerializer(queryset,many=True)
            return Response(serializer.data)
        else :
            return Response(False)
    @action(methods=['POST'],detail=False,url_path='user',url_name='post_user')
    def post_user(self, request, *arg, **kwargs):
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            birthday = request.POST.get('birthday')
            print(request.POST)
            userCreate =  User.objects.create(name=name,username=username,phone=phone,email=email)
            userCreate.password =make_password(password)
            customer = Customer(name=name, address=address,
                                    email=email, birthday=birthday)
            customer.save()
            userCreate.customer_id = customer
            userCreate.save()
        queryset = User.objects.filter(username=username,password=password)
        
        serializer = UserSerializer(queryset,many=True)
        return Response(serializer.data)
    @action(methods=['PUT'],detail=False , url_path="user",url_name="put_user")
    def put_user (self,request,*args , **kwargs):
        user = request.PUT.get('user')
        return Response(user)