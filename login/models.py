from django.db import models
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Store(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    address = models.TextField()
    city = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    fax = models.CharField(max_length=50)
    email = models.EmailField()
    logo = models.ImageField(null=True,blank=True)

class Customer(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=50)
    birthday = models.DateField()

    def __str__(self):
        return self.name
class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True, null=True)
    phone = models.CharField(max_length=10)
    avatar = models.ImageField(null=True, default="avatar.svg")
    password = models.CharField(max_length=200)
    store_id = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True,related_name='users')
    customer_id = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True,related_name='users')

    USERNAME_FIELD = 'username'
    def __str__(self):
        return self.username
class Feedback(models.Model):
    id = models.BigAutoField(primary_key=True)
    reason = models.CharField(max_length=200,null=True)
    note = models.TextField(null=True)
    replay = models.TextField(null=True)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
