from django.shortcuts import render,redirect
from django.urls import reverse
from product.models import Categories
from paypal.standard.forms import PayPalPaymentsForm
from django.contrib import messages
from product.models import Product
from django.conf import settings
from order.models import Order,Detail_order,Transport
import uuid 
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
import datetime
import string
import random

@login_required
def paymentPage (request):
    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    list_category = Categories.objects.all()
    productPay = str(request.GET['productPay']).split('_')
    current = request.user
    customer = current.customer_id
    host = request.get_host()
    product = []
    transport = Transport.objects.get(slug=request.GET['transport'])
    order = Order(
            name=slugify(""+customer.name+"-"+id_generator()),
            datetime=datetime.datetime.now(),
            receiver=customer.name,
            address_receiver=customer.address,
            phone_receiver=current.phone,
            status=False,
            customer_id=customer
        )
    order.save()
    total=transport.price
    for item in productPay:
        if(item != ""):
            quantity=item.replace(":", "-").split("-")[-1]
            size = item.replace(":", "-").split("-")[-2]
            slug = item.replace("-"+size+":"+quantity, "")
            product_item = Product.objects.filter(sizes__isnull=False,sizes__size=size,slug=slug,sizes__quantity__gte=quantity,
                                                  prices__isnull=False,photo_products__isnull=False).values(
                'prices__price','sizes__quantity','id','name', 'sex', 'prices__price', 'prices__sale', 'photo_products__name', 'photo_products__data'
            )
            if product_item != []:
                total+= float(product_item[0]['prices__price'])*float(quantity)
                detail_order = Detail_order.objects.get(product_id=product_item[0]['id'],size=size,quantity=quantity)
                if detail_order:
                    product_add = dict()
                    product_add['prices__price'] = product_item[0]['prices__price']
                    product_add['name'] = product_item[0]['name']
                    product_add['sex'] = product_item[0]['sex']
                    product_add['photo_products__name'] = product_item[0]['photo_products__name']
                    product_add['quantity'] = quantity
                    product.append(product_add)
                    detail_order.order_id=order
            
    order.total_price=total
    print(total)
    order.save()
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": str(total/23631),
        "item_name": order.name,
        "invoice": str(order),
        "curency_code" : "USD",
        "notify_url":  f'http://{host}{reverse("paypal-ipn")}',
        "return_url":  f'http://{host}{reverse("paypal-reverse")}',
        "cancel_return":  f'http://{host}{reverse("paypal-cancel")}',
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request,'test.html',{'list_category':list_category,'form':form ,'current': current ,
                                       'customer': customer, 'product':product,'order':order, 'transport': transport,
                                       
                                       })
def paypal_return(request):
    messages.success(request,"successfully make a payment")
    return redirect('payment')
def paypal_reverse(request):
    print(request.GET)
    return redirect('payment')
def paypal_cancel(request):
    return redirect('payment')