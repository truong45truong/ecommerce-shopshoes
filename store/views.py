from django.shortcuts import render,redirect
from login.models import Store
from product.models import Product,Categories
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from product.filters import ProductFilter
from django.shortcuts import render,redirect,HttpResponse
from order.models import Order,Detail_order
from payment.models import Process_order
from login.views import upload,handleImageUpload
from login.forms import ImageStoreForm
from  datetime import datetime
import json
 
@login_required
def myStorePage(request):
    try :
        list_category = Categories.objects.all()
        dataStore = Store.objects.filter(users__username=request.user)
        print(dataStore[0])
    except:
        pass
    order = []
    try :
        process_order = Process_order.objects.filter(process= 1 , store_id = dataStore[0])
        print(process_order)
        for item in process_order : 
            order_item = Order.objects.filter(id=item.order_id.id ,cancel=False,request_cancel =False ,payments__isnull = False).values(
                'name','total_price','payments__allowed','datetime','payments__qrcode__token'
            )
            print(item)
            if order_item[0]:
                order.append(order_item[0])
                print(order_item)
    except :
        pass
    
    order_cancel = []
    try :
        process_order_cancel = Process_order.objects.filter( store_id = dataStore[0])
        for item in process_order_cancel : 
            order_item = Order.objects.filter(id=item.order_id.id ,payments__isnull = False ,cancel=True).values(
                'name','total_price','payments__allowed','datetime','payments__qrcode__token'
            )
            if order_item:
                order_cancel.append(order_item[0])
    except :
        pass
    
    order_request_cancel = []
    try :
        process_order_request_cancel = Process_order.objects.filter( store_id = dataStore[0])
        for item in process_order_request_cancel : 
            order_item = Order.objects.filter(id=item.order_id.id ,payments__isnull = False ,request_cancel=True).values(
                'name','total_price','payments__allowed','datetime','payments__qrcode__token'
            )
            if order_item:
                order_request_cancel.append(order_item[0])
    except :
        pass
    
    formImage  = ImageStoreForm()
    if request.POST :
        formImage  = ImageStoreForm(request.POST,request.FILES)
        nameUpdate = request.POST.get('name-update')
        emailUpdate = request.POST.get('email-update')
        phoneUpdate = request.POST.get('phone-update')
        addressUpdate = request.POST.get('address-update')
        cityUpdate = request.POST.get('city-update')
        contactUpdate = request.POST.get('contact-update')
        
        storeUpdate = Store.objects.get(id=dataStore[0].id)
        storeUpdate.email = emailUpdate
        storeUpdate.name = nameUpdate
        storeUpdate.phone = phoneUpdate
        storeUpdate.address = addressUpdate
        storeUpdate.city = cityUpdate
        storeUpdate.contact = contactUpdate
        storeUpdate.logo = str(storeUpdate.id)+'brand'+".png"
        storeUpdate.save()
        
        if formImage.is_valid():
            logo = request.FILES['data']
            print('img',logo)
            upload(logo,str(storeUpdate.logo))
            handleImageUpload(str(storeUpdate.logo))
    
        
    if(len(dataStore)==0):
        return redirect('registerstore')
    else:
        return render(request,'storeInfo.html',{ 
                                                'dataStore':dataStore[0] ,'current' : request.user ,
                                                'formImage':formImage,
                                                'list_category': list_category,
                                                'order' : order , 'order_cancel' : order_cancel,
                                                'order_request_cancel' :order_request_cancel
                                                })


def detailStorePage(request,slugstore):
    list_product = Product.objects.filter(
        prices__isnull=False, photo_products__isnull=False).values(
        'name', 'slug', 'sex', 'prices__price', 'prices__sale', 'photo_products__name', 'prices__price_total', 'category_id__logo')
    filtered_qs = ProductFilter(request.GET, queryset=list_product).qs
    paginator = Paginator(filtered_qs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if (request.user.is_anonymous is False):
        return render(request,'storeDetail.html',{'page_obj': page_obj, 'pages': range(1, page_obj.paginator.num_pages), 'current' :request.user,'store': True})
    else :
        return render(request,'storeDetail.html',{ 'page_obj': page_obj, 'pages': range(1, page_obj.paginator.num_pages),'current' : False ,'store': True})


@login_required
def statisticOrder(request):
    order=[]
    total = 0
    number_order= 0
    if request.GET:
        date_start = datetime.fromisoformat(request.GET['date_start'])

        date_end =datetime.fromisoformat(request.GET['date_end'])
        
        try :
            process_order = Process_order.objects.filter( store_id = request.user.store_id)
            for item in process_order : 
                order_item = Order.objects.filter(id=item.order_id.id ,payments__isnull = False,
                            datetime__gte = date_start , datetime__lte = date_end , cancel=False
                    ).values(
                    'name','total_price','payments__allowed','datetime','payments__qrcode__token'
                )
                if order_item:
                    total += order_item[0]['total_price']
                    number_order += 1
                    order.append(order_item[0])
            order = sorted(order, key=lambda values: values['datetime'])
        except :
            pass
        return render(request,'statisticResultOrder.html',{'order' : order , 'date_start' : request.GET['date_start'] , 'date_end' : request.GET['date_end'] ,
                                                           'total': total , 'number_order' : number_order
                                                        })

@csrf_exempt
def getValueChart(request):
    data= json.loads(request.body.decode('utf-8'))
    print(data)
    if data['post'] is True:
        order=[]
        date_start = datetime.fromisoformat(data['date_start'])
        date_end =datetime.fromisoformat(data['date_end'])
        try :
            process_order = Process_order.objects.filter( store_id = request.user.store_id)
            for item in process_order : 
                order_item = Order.objects.filter(id=item.order_id.id ,payments__isnull = False,
                            datetime__gte = date_start , datetime__lte = date_end ,cancel=False
                    ).values(
                    'total_price','datetime'
                )
                    
                if order_item:
                    dat= json.dumps(order_item[0]['datetime'],default=str)
                    order.append({'x': dat,'y': order_item[0]['total_price']})
        except :
            pass
    return HttpResponse(json.dumps(order))

