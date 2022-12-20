from django.contrib import admin
from .models import Transport, Order, Detail_order
# Register your models here.

admin.site.register(Transport)
admin.site.register(Order)
admin.site.register(Detail_order)