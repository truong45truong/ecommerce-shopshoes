from django.db import models
from product.models import Product
from login.models import Customer
# Create your models here.

class Transport(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    logo = models.ImageField(null=True)
    price = models.FloatField(null=True)

class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    datetime = models.DateTimeField()
    receiver = models.CharField(max_length=50,null=True)
    address_receiver = models.CharField(max_length=200,null=True)
    phone_receiver = models.CharField(max_length=10,null=True)
    status = models.BooleanField()
    total_price = models.FloatField(null=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    transport_id = models.ForeignKey(Transport, on_delete=models.SET_NULL, null=True)

class Detail_order(models.Model):
    id = models.BigAutoField(primary_key=True)
    status = models.BooleanField()
    quantity = models.IntegerField()
    order_id = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True,related_name='detail_orders')
    product_id = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

