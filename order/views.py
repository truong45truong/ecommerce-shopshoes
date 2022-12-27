from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Order, Detail_order,Transport
from payment.models import Payment, Process_order
from product.models import Product,Categories,Evaluate
from login.models import Customer, User
from django.contrib.auth.hashers import check_password
from django.shortcuts import HttpResponse
from django.template.defaultfilters import slugify
import json
import datetime
import random
import string
# Create your views here.

@login_required
def getProductOfUser(request, data):
    current_user = request.user
    if current_user.is_authenticated:
        user = User.objects.get(username=current_user)
        customer = Customer.objects.filter(users__username=user)
        product_cart_user = Detail_order.objects.filter(customer_id=customer[0],order_id__isnull=True).values(
            'product_id','quantity','size'
        )
        
        for item in product_cart_user:
            data.append({
                'slug': Product.objects.get(id=item['product_id']).slug,
                'quantity': item['quantity'],
                'size' : item['size'],
            })
    return data
def handleDuplicateProducts(data):
    print(data)
    def checkInside(size,dirSize):
        for index in  range(len(dirSize)):
                if size == dirSize[index]['size'] :
                    return True
        return False
    dir = dict()
    for item in data:
        if item['slug'] in dir :
            for index in  range(len(dir[item['slug']][:])):
                if item['size'] == dir[item['slug']][index]['size'] :
                    dir[item['slug']][index]['quantity'] = int(dir[item['slug']][index]['quantity']) + int(item['quantity'])
                    break
                else :
                    if checkInside(item['size'],dir[item['slug']][:]) == False :
                        dir[item['slug']].append({'quantity' : item['quantity'] ,'size' : item['size']})
        else:
            dir[item['slug']] = [{'quantity' : item['quantity'] ,'size' : item['size']}]
    return dir
def processingSynthesisProduct(data):
    list_product = []
    total_price = 0
    for i in data.keys():
        for index in range(len(data[i])):
            item = Product.objects.filter(
                prices__isnull=False, photo_products__isnull=False, slug=i,sizes__isnull=False,sizes__size=data[i][index]['size']).values(
                'name', 'slug', 'sex', 'prices__price', 'prices__sale',
                'photo_products__name', 'prices__price_total', 'category_id__logo' , 'sizes__size' , 'sizes__quantity'
            )
            if len(item) ==1 :    
                list_product.append(
                    {
                        'name': item[0]['name'],
                        'slug': item[0]['slug'],
                        'sex': item[0]['sex'],
                        'sale': item[0]['prices__sale'],
                        'photo': item[0]['photo_products__name'],
                        'price_total': item[0]['prices__price_total'],
                        'category': item[0]['category_id__logo'],
                        'size': item[0]['sizes__size'],
                        'quantity' : data[i][index]['quantity'],
                        'quantityMax' : item[0]['sizes__quantity'],
                    }
                )
        # total_price = total_price + \
        #     int(data[i])*float(item[0]['prices__price_total'])
    return 0, list_product
@csrf_exempt
def shoppingCartPage(request):
    list_category=Categories.objects.all()

    try:
        data = request.session['cart']
    except Exception:
        data = []
    getProductOfUser(request, data)
    dir_product_cart = handleDuplicateProducts(data)
    total_price, products = processingSynthesisProduct(dir_product_cart)
    list_trainsport = Transport.objects.all()
    if (request.user.is_authenticated is True):
        return render(request, 'shoppingcart.html', {
                                                     'product': products, 'total_price': total_price,
                                                     'current' : request.user ,'list_category':list_category,
                                                     'list_trainsport':list_trainsport,
                                                     })
    else :
        return render(request, 'shoppingcart.html', {'product': products, 'total_price': total_price,
                                                     'list_category': list_category, 'list_trainsport':list_trainsport,'current':False})

def add_to_cart(request):

    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def add_with_account(request):
        user = User.objects.get(username=request.user)
        customer = user.customer_id
        
        detail_order = Detail_order(
            status=False, quantity=data['quantity'], product_id=product,size = data['sizes'],customer_id=customer)
        detail_order.save()


    def add_with_session(request):
        try:
            data_cart = request.session['cart']
        except:
            data_cart = []
        item_cart = {
            'slug' : data['slug'],
            'size' : int(data['sizes']),
            'quantity' : data['quantity'] 
        }
        data_cart.append(item_cart)
        request.session['cart'] = data_cart
        print(data_cart)
    
    data = json.loads(request.body.decode('utf-8'))
    product = Product.objects.get(slug=data['slug'])
    
    if request.user.is_authenticated:
        add_with_account(request)
    else:
        add_with_session(request)
    return HttpResponse(str(data))


@csrf_exempt
def remove_to_cart (request):
    data = json.loads(request.body.decode('utf-8'))
    product = Product.objects.get(slug=data['slug'])
    size = data['sizes']
    current_user = request.user
    
    if current_user.is_authenticated:
        user = User.objects.get(username=current_user)
        customer = Customer.objects.filter(users__username=user)
        product_cart_user = Detail_order.objects.filter(customer_id=customer[0],product_id=product,size=size).values(
            "id" 
        )
        for item in product_cart_user:
                Detail_order.objects.get(id=item['id']).delete()
                print("delete sucess")
    try:
        dataSession = request.session['cart']
        if(dataSession != []):
            for item in dataSession :
                dataSession.remove(item)
            request.session['cart'] = dataSession
    except Exception:
        request.session['cart'] = []
    dataSession = request.session['cart']
    print("session",dataSession)
    dataUser = getProductOfUser(request, dataSession)
    dir_product_cart = handleDuplicateProducts(dataUser)
    total_price, products = processingSynthesisProduct(dir_product_cart)
    return HttpResponse(json.dumps(products))
@login_required
def ViewOrder(request, order_name):
    list_category=Categories.objects.all()
    order = Order.objects.get(name=order_name)
    process_order = Process_order.objects.get(order_id=order.id)
    store = process_order.store_id
    product = []
    product_cart_user = Detail_order.objects.filter(customer_id=request.user.customer_id,order_id=order).values(
            'product_id','quantity','size'
        )
    customer = request.user.customer_id
    for item in product_cart_user:
        items = Product.objects.filter(
                prices__isnull=False, photo_products__isnull=False, id=item['product_id']).values(
                'name', 'slug', 'sex', 'prices__price', 'prices__sale',
                'photo_products__name', 'prices__price_total', 'category_id__logo'
            )
        product.append({
            'name': items[0]['name'],
            'quantity': item['quantity'],
            'size' : item['size'],
            'sex': items[0]['sex'],
            'prices__price': items[0]['prices__price'],
            'prices__price_total' : items[0]['prices__price_total'],
            'prices__sale': items[0]['prices__sale'],
            'photo_products__name' : items[0]['photo_products__name'],
        })
    if request.POST :
        if process_order.process == 5:
            for item in product_cart_user:
                print(item)
                eval = Evaluate.objects.create(description=request.POST['prorcess6'],product_id=Product(id=item['product_id']),
                                            user_id = request.user,datetime_create=datetime.datetime.now()
                                            )
                eval.save()
            process_order.process6 = request.POST['prorcess6']
            process_order.process = 6
            process_order.save()
        try:
            if request.POST['request-cancel']:
                print("request cancel")
                order.request_cancel=True
                order.save()
        except:
            pass
            

    return render(request,'order.html',{'list_category' : list_category ,'product' : product ,
                                        'customer' : customer ,'order' : order ,'current' : request.user
                                        ,'process_order' : process_order ,'order_name' :order_name,
                                        'store' :store
                                        })