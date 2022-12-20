from django.db import models
from login.models import Store,User
from mptt.models import MPTTModel, TreeForeignKey
# Create your models here.

class Categories(MPTTModel):
    id = models.BigAutoField(primary_key=True)
    slug = models.CharField(null=False,max_length=50,unique=True)
    name=models.CharField(max_length=50)
    logo=models.ImageField(null=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name
class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    slug = models.CharField(null=False,max_length=50)
    name=models.CharField(max_length=50,null=False)
    sex = models.IntegerField(null=True)
    description=models.TextField(null=True)
    store_id=models.ForeignKey(Store, on_delete=models.SET_NULL, null=True)
    category_id=models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
        
class Size(models.Model):
    id = models.BigAutoField(primary_key=True)
    size= models.IntegerField()
    quantity = models.IntegerField(null=True)
    product_id = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True,blank=True,related_name='sizes')

    def __str__(self):
        return self.product_id.name +"-"+ str(self.size)

class Evaluate(models.Model):
    id = models.BigAutoField(primary_key=True)
    rate=models.FloatField()
    description=models.TextField(null=True)
    user_id=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product_id = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

class Price(models.Model):
    id = models.BigAutoField(primary_key=True)
    price=models.FloatField(null=True)
    sale=models.FloatField(null=True)
    status=models.BooleanField(null=True)
    datetime_create=models.DateTimeField(null=True)
    price_total=models.FloatField(null=True)
    product_id = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True,blank=True,related_name='prices')



class Photo_product(models.Model):
    id = models.BigAutoField(primary_key=True)
    name=models.CharField(max_length=50,null=True)
    data=models.ImageField()
    product_id = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True,blank=True,related_name='photo_products')

    fields = ['data']
