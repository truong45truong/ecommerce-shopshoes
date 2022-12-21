from django.shortcuts import render,redirect
from django.urls import reverse
from product.models import Categories
from paypal.standard.forms import PayPalPaymentsForm
from django.contrib import messages
from django.conf import settings
import uuid 
def paymentPage (request):
    list_category = Categories.objects.all()
    host = request.get_host()
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": "20.00",
        "item_name": "Product 1",
        "invoice": str(uuid.uuid4()),
        "curency_code" : "USD",
        "notify_url":  f'http://{host},{reverse("paypal-ipn")}',
        "return_url":  f'http://{host},{reverse("paypal-reverse")}',
        "cancel_return":  f'http://{host},{reverse("paypal-cancel")}',
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request,'test.html',{'list_category':list_category,'form':form})
def paypal_return(request):
    messages.success(request,"successfully make a payment")
    redirect('payment')
def paypal_reverse(request):
    redirect('payment')
def paypal_cancel(request):
    redirect('payment')