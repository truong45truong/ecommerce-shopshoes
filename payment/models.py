from django.db import models
from order.models import Order

# Create your models here.
class Payment(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.IntegerField()
    allowed = models.BooleanField()
    datetime = models.DateTimeField()
    order_id = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True,blank=True,related_name='detailorders')

