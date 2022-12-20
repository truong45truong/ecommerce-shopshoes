from django.contrib import admin
from .models import User,Store,Customer,Feedback
# Register your models here.

admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Store)
admin.site.register(Feedback)