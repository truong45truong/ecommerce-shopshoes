from django.shortcuts import render
from product.models import Categories

def paymentPage (request):
    list_category = Categories.objects.all()
    return render(request,'payment.html',{'list_category':list_category,})
