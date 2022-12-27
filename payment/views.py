from django.shortcuts import render,redirect
from django.urls import reverse
from product.models import Categories
from paypal.standard.forms import PayPalPaymentsForm
from django.contrib import messages
from product.models import Product
from .models import Qrcode,Payment,Process_order
from django.shortcuts import HttpResponse
from login.models import User,Store
from django.conf import settings
from order.models import Order,Detail_order,Transport
import uuid 
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from django.views.decorators.csrf import csrf_exempt
import datetime
import string
import random
import json
import uuid
def RemoveOrderCash(customer):
    orders = Order.objects.filter(customer_id=customer,status=False)
    for item in orders:
        try:
            payment = Payment.objects.get(order_id=item)
            qrcode = Qrcode.objects.get(id=payment.qrcode.id)
            order = Order.objects.get(id=item.id)
            process_order = Process_order.objects.get(order_id=order)
            payment.delete()
            qrcode.delete()
            order.delete()
            process_order.delete()
        except:
            pass
@login_required
def paymentPage (request):
    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def checkOrder(data_product):
        store_check = False
        for item in productPay:
            if(item != ""):
                quantity=item.replace(":", "-").split("-")[-1]
                size = item.replace(":", "-").split("-")[-2]
                slug = item.replace("-"+size+":"+quantity, "")
                if store_check == False:
                    store_check = Product.objects.get(slug=slug).store_id
                else:
                    if store_check != Product.objects.get(slug=slug).store_id :
                        return False
                    
    list_category = Categories.objects.all()
    productPay = str(request.GET['productPay']).split('_')
    if checkOrder(productPay) == False :
        return render(request, 'check.html', 
                          {'error': 'Hãy mua những sản phẩn cùng cửa hàng!', 'cd':False,'list_category':list_category})
    store_check=""
    
    current = request.user
    customer = current.customer_id
    RemoveOrderCash(customer)
    host = request.get_host()
    product = []
    transport = Transport.objects.get(slug=request.GET['transport'])
    order = Order(
            name=slugify(""+customer.name+"-"+id_generator()+"-"+str(uuid.uuid4())),
            datetime=datetime.datetime.now(),
            receiver=customer.name,
            address_receiver=customer.address,
            phone_receiver=current.phone,
            status=False,
            customer_id=customer,
            transport_id = transport,
            request_cancel=False,
            cancel=False
        )

    order.save()
    process_order = Process_order.objects.create(order_id=order,process=1)
    process_order.process1="customer name: "+ customer.name + "customer id:" + str(customer.id) +" datecreate: " +str(datetime.datetime.now())
    process_order.save()
    total=transport.price
    for item in productPay:
        if(item != ""):
            quantity=item.replace(":", "-").split("-")[-1]
            size = item.replace(":", "-").split("-")[-2]
            slug = item.replace("-"+size+":"+quantity, "")
            product_item = Product.objects.filter(sizes__isnull=False,sizes__size=size,slug=slug,sizes__quantity__gte=quantity,
                                                  prices__isnull=False,photo_products__isnull=False).values(
                'prices__price','sizes__quantity','id','name', 'sex', 'prices__price', 'prices__sale', 
                'photo_products__name', 'photo_products__data', 'store_id'
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
                    detail_order.save()
                    process_order.store_id = Store.objects.get(id=product_item[0]['store_id'])
                    process_order.save()
            
    order.total_price=total
    print(total)
    order.save()
    qrcode = Qrcode.objects.create()
    qrcode.name=request.user.name
    qrcode.save()
    payment = Payment.objects.create(type=0,datetime=datetime.datetime.now(),allowed = False,slug=uuid.uuid4())
    payment.qrcode = qrcode
    payment.order_id=order
    payment.save()
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": str(total/23631),
        "item_name": order.name,
        "invoice": str(payment.id),
        "curency_code" : "USD",
        "notify_url":  f'http://{host}{reverse("paypal-ipn")}',
        "return_url":  f'http://{host}{reverse("paypal-reverse")}',
        "cancel_return":  f'http://{host}{reverse("paypal-cancel")}',
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request,'test.html',{'list_category':list_category,'form':form ,'current': current ,
                                       'customer': customer, 'product':product,'order':order, 'transport': transport,
                                       'slug':payment.slug, 
                                       })
def paypal_return(request,sender, **kwargs):
    messages.success(request,"successfully make a payment")
    ipn_obj = sender
    # Retrieve the order_number previously passed
    order_number = ipn_obj.invoice
    # Get the order :D
    order = Order.objects.get(order_number=order_number)
    list_category = Categories.objects.all()
    return render(request, 'check.html', 
                          {'error': order_number, 'cd':True,'list_category':list_category})
    
def paypal_reverse(request,sender, **kwargs):
    messages.success(request,"successfully make a payment")
    ipn_obj = sender
    # Retrieve the order_number previously passed
    order_number = ipn_obj.invoice
    # Get the order :D
    order = Order.objects.get(order_number=order_number)
    list_category = Categories.objects.all()
    return render(request, 'check.html', 
                          {'error': order_number, 'cd':True,'list_category':list_category})

def paypal_cancel(request):
    return redirect('payment')

@login_required
def qrcodePage(request,token):
    list_category = Categories.objects.all()
    current = User.objects.filter(id = request.user.id).values(
        'is_staff'
    )
    if current[0]['is_staff'] == True : 
    
        qrcode = Qrcode.objects.get(token=token)
        payment = Payment.objects.get(qrcode = qrcode)
        process_order = Process_order.objects.get(order_id=payment.order_id)
        order = Order.objects.get(id=payment.order_id.id)
        process_order.save()
        if request.GET :
            try :
                payment_cancel = request.GET['payment-cancel']
                if payment_cancel:
                    order = Order.objects.get(name=payment_cancel)
                    order.cancel = True
                    order.save()
                    return HttpResponse('Hủy đơn thành công')
            except:
                pass
            confirm = request.GET['confirm']
            print("confirm",confirm)
            if confirm == "2" and process_order.process1 != None and process_order.process2 == None:
                if process_order.process3 == None and process_order.process4 == None :
                    if process_order.process5 == None and process_order.process6 == None :
                        info = "id user : " + str(request.user.id) + "\n" 
                        info += "datetime Create :" + str(datetime.datetime.now())  + "\n" 
                        info += "name confirm: " + request.user.name
                        process_order.process2=info
                        process_order.process=2
                        
            if confirm == "3" and process_order.process1 != None and process_order.process2 != None:
                if process_order.process3 == None and process_order.process4 == None :
                    if process_order.process5 == None and process_order.process6 == None :
                        info = "id user : " + str(request.user.id) + "\n" 
                        info += "datetime Create :" + str(datetime.datetime.now())  + "\n" 
                        info += "name confirm: " + request.user.name
                        process_order.process3=info
                        process_order.process=3
                        
            if confirm == "4" and process_order.process1 != None and process_order.process2 != None:
                if process_order.process3 != None and process_order.process4 == None :
                    if process_order.process5 == None and process_order.process6 == None :
                        info = "id user : " + str(request.user.id) + "\n" 
                        info += "datetime Create :" + str(datetime.datetime.now()) +  "\n" 
                        info += "name confirm: " + request.user.name
                        process_order.process4=info
                        process_order.process=4
                        
            if confirm == "5" and process_order.process1 != None and process_order.process2 != None:
                if process_order.process3 != None and process_order.process4 != None :
                    if process_order.process5 == None and process_order.process6 == None :
                        info = "id user : " + str(request.user.id) + "\n" 
                        info += "datetime Create :" + str(datetime.datetime.now()) + "\n" 
                        info += "name confirm: " + request.user.name
                        process_order.process5=info
                        process_order.process=5
                        payment.allowed = True
                        payment.save()
            if confirm == "6" and process_order.process1 != None and process_order.process2 != None:
                if process_order.process3 != None and process_order.process4 != None :
                    if process_order.process5 != None and process_order.process6 == None :
                        info = request.GET['prorcess6']
                        process_order.process6=info
                        process_order.process=6
                        
        process_order.save()
        print("process_order.process",process_order.process)
        return render(request,'qrcode.html',{'qrcode':qrcode ,'list_category' : list_category,
                                          'current' : request.user ,'process_order':process_order,
                                          'token' : token, 'order' : order
                                         })
    else :
        redirect('home')
      
@login_required  
@csrf_exempt
def payOnReceipt(request):
    list_category = Categories.objects.all()
    def delete():
        qrcode = Qrcode.objects.get(id=payment.qrcode.id)
        process_order = Process_order.objects.get(order_id=order)
        payment.delete()
        qrcode.delete()
        order.delete()
        process_order.delete()
    try :
        customer = request.user.customer_id
        data = json.loads(request.body.decode('utf-8'))
        payment = Payment.objects.get(slug=data['slug'])
        order = Order.objects.get(id=payment.order_id.id)
        product = Detail_order.objects.filter(order_id = order)
        print(product)
        if product:
            order.status = True
            print(order)
            order.save()
            RemoveOrderCash(customer)
        else:
            delete()
            return render(request, 'check.html', 
                          {'error': 'Mua hàng thất bại!', 'cd':False,'list_category':list_category})
    except:
        return render(request, 'check.html', 
                          {'error': 'Mua hàng thất bại!', 'cd':False,'list_category':list_category})
    return render(request, 'check.html', 
                          {'error': 'Mua hàng thành công!', 'cd':True,'list_category':list_category})

@login_required  
@csrf_exempt
def removePayment(request):
    try :
        # customer = request.user.customer_id
        # data = json.loads(request.body.decode('utf-8'))
        # payment = Payment.objects.get(slug=data['slug'])
        # order = Order.objects.filter(id=payment.order_id.id,status=False)
        # product = Detail_order.objects.get(order_id = order[0])
        # print(product)
        # product.order_id = None
        # product.save()
        pass
    except:
        pass
