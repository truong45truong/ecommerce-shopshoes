from django.contrib import admin
from .models import Payment,Qrcode,Process_order
# Register your models here.
admin.site.register(Payment)
admin.site.register(Qrcode)
admin.site.register(Process_order)