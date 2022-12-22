from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProductForm, PriceForm, PhotoProductForm
from .models import Categories, Photo_product, Product, Price, Size, Evaluate
from login.models import User,Store , Customer
from django.core.paginator import Paginator
from .filters import ProductFilter
from django.template.defaultfilters import slugify
from django.db.models import Min, Max
import os
import shutil
import datetime
import random
import string
import json
from django.conf import settings
# path save photo

path_upload = str(settings.BASE_DIR)+"/media_upload/photos"
path_root = str(settings.BASE_DIR)+"/media/photos"
# Create your views here.


def productPage(request, slug):
    list_category=Categories.objects.all()
    sex = request.GET.get('sexselect')
    minprice = Product.objects.all().aggregate(Min('prices__price_total'))
    maxprice = Product.objects.all().aggregate(Max('prices__price_total'))
        
    sortby = request.GET.get('sortby')
    # prod=Product.objects.all()
    name_arr = '-id'
    if sortby == "lastest":
        name_arr ='-id'
    if sortby == "highrate":
        name_arr = 'id'
    if sortby == "lowtohigh":
        name_arr = 'prices__price_total'
    if sortby == "hightolow":
        name_arr = '-prices__price_total'
        
    if slug=='0':
        list_product = Product.objects.filter(
        prices__isnull=False, photo_products__isnull=False).values(
        'name', 'slug', 'sex', 'prices__price', 'prices__sale', 'photo_products__name', 'photo_products__data', 'prices__price_total', 'category_id__logo').order_by(name_arr)
        filtered_qs = ProductFilter(request.GET, queryset=list_product).qs
    else:
        list_product = Product.objects.filter(
        prices__isnull=False, category_id__slug=slug, photo_products__isnull=False).values(
        'name', 'slug', 'sex', 'prices__price', 'prices__sale', 'photo_products__name', 'photo_products__data', 'prices__price_total', 'category_id__logo').order_by(name_arr)
        filtered_qs = ProductFilter(request.GET, queryset=list_product).qs
        
    filterPrice = request.GET.get('filterPrice')
    if filterPrice:
        int_filterPrice = int(filterPrice)
        list_product = list_product.filter(prices__price_total__lte=int_filterPrice).order_by(name_arr)
        filtered_qs = ProductFilter(request.GET, queryset=list_product).qs
        
    
    if sex:
        list_product = list_product.filter(sex=sex).order_by(name_arr)
        filtered_qs = ProductFilter(request.GET, queryset=list_product).qs
        
        
    paginator = Paginator(filtered_qs, 8)
    page_number = request.GET.get('page') if request.GET.get('page') != None else '1'
    page_obj = paginator.get_page(page_number)
    nums = "a" * page_obj.paginator.num_pages
    if (request.user.is_anonymous is False):
        return render(request,'Product.html',{'products': page_obj, 'pages': range(1, page_obj.paginator.num_pages), 
                                              'current' :request.user,'store': True, 'nums':nums,
                                              'list_category':list_category, 'sortby':sortby, 
                                              'minprice':minprice, 'maxprice':maxprice, 'filterPrice':filterPrice,
                                              })
    else :
        return render(request,'Product.html',{ 'products': page_obj, 'pages': range(1, page_obj.paginator.num_pages),
                                              'current' : False ,'store': True, 'nums':nums,
                                              'list_category':list_category, 'sortby': sortby,
                                              'minprice':minprice, 'maxprice':maxprice, 'filterPrice':filterPrice,
                                              })


def productDetail(request, slug):
    list_category = Categories.objects.all()
    
    product = Product.objects.get(prices__isnull=False, slug=slug)
    priceProduct = Price.objects.get(product_id__slug=slug)
    storeInfo = Store.objects.get(id=product.store_id.id)
    list_size = Size.objects.filter(product_id__slug=slug)
    imgProduct = Photo_product.objects.filter(product_id__slug=slug)
    evaluate = Evaluate.objects.filter(product_id__slug=slug)
    
    list_product = Product.objects.filter(
        prices__isnull=False, photo_products__isnull=False).values(
    # prices__isnull=False).values(
    'name', 'slug', 'sex', 'prices__price', 'prices__sale', 'photo_products__name', 'photo_products__data', 'prices__price_total', 'category_id__logo').order_by('id')
    filtered_qs = ProductFilter(request.GET, queryset=list_product).qs
    
    paginator = Paginator(filtered_qs, 4)
    page_number = request.GET.get('page') if request.GET.get('page') != None else '1'
    page_obj = paginator.get_page(page_number)
    nums = "a" * page_obj.paginator.num_pages
    
    if (request.user.is_anonymous is False):
        return render(request,'ProductDetail.html',
                      {'current' :request.user,
                    'list_category':list_category, 'product':product, 'list_size':list_size, 'imgProduct':imgProduct,
                    'page': int(page_number), 'products': page_obj, 'priceProduct':priceProduct, 'storeInfo':storeInfo,
                    'evaluate':evaluate,
                    })
    else :
        return render(request,'ProductDetail.html',
                    {'current' : False ,
                    'list_category':list_category, 'product':product, 'list_size':list_size, 'imgProduct':imgProduct,
                    'page': int(page_number), 'products': page_obj, 'priceProduct':priceProduct, 'storeInfo':storeInfo,
                    })

@login_required
def productNewPage(request):
    print(settings.BASE_DIR)
    list_category=Categories.objects.all()
    
    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    userCurrent = User.objects.get(username=request.user)
    if userCurrent.store_id:
        form_product = ProductForm()
        form_price = PriceForm()
        form_photoproduct = PhotoProductForm()
        if request.method == 'POST':
            form_price = PriceForm(request.POST)
            form_photoproduct = PhotoProductForm(request.POST, request.FILES)
            form_product = ProductForm(request.POST)
            if form_product.is_valid():
                name = form_product.cleaned_data['name']
                sex = form_product.cleaned_data['gender']
                description = form_product.cleaned_data['description']
                category = form_product.cleaned_data['category_id']
                while True:
                    try:
                        product = Product(name=name, sex=sex, description=description,
                                        category_id=category, slug=slugify(
                                            name) + "-" + id_generator(),store_id=userCurrent.store_id
                                        )
                        break
                    except:
                        pass
                product.save()
                for i in range(35, 45):
                    quantity = request.POST.get('sizevalue_' + str(i))
                    Size(size=i, quantity=quantity, product_id=product).save()

            if form_price.is_valid():
                price = form_price.cleaned_data['price']
                sale = form_price.cleaned_data['sale']
                price_product = Price(price=price, sale=sale, price_total=(100-float(sale))*float(price)/100,
                                    product_id=Product(id=product.id), datetime_create=datetime.datetime.now()
                                    )
        

                price_product.save()
            if form_photoproduct.is_valid():
                upload(request.FILES['data'], product.id)
                handleImageUpload(request.FILES['data'], product.id)
        return render(request, 'Productnew.html', {'form_product': form_product, 
                                                   'form_price': form_price, 
                                                   'form_photoproduct': form_photoproduct, 
                                                   'current' :request.user,'store': True,
                                                   'list_category':list_category,
                                                   })

    return  render(request, 'noHaveAccountStore.html',{'current' :request.user,'store': True})


def upload(f, product):
    if (f.name.split('.')[-1] in ['png', 'jpg', 'webp']):
        file = open(
            os.path.join(path_upload, "products", str(
                product) + '.' + f.name.split('.')[-1]),
            'wb+'
        )
        for chunk in f.chunks():
            file.write(chunk)
        file.close()
    # code handle upload


def handleImageUpload(f, product):
    nameFile = str(product) + '.' + f.name.split('.')[-1]
    shutil.move(path_upload + '/products' + '/' + nameFile,
                path_root + '/products' + '/' + nameFile)
    photo_product = Photo_product(
        name=nameFile, data=nameFile, product_id=Product(id=product))
    photo_product.save()
