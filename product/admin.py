from django.contrib import admin
from .models import Product, Price, Photo_product, Evaluate, Categories, Size
# Register your models here.
admin.site.register(Price)
admin.site.register(Product)
admin.site.register(Photo_product)
admin.site.register(Evaluate)
admin.site.register(Categories)
admin.site.register(Size)