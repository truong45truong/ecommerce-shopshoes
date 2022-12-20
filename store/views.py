from django.shortcuts import render,redirect
from login.models import Store
from product.models import Product,Categories
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from product.filters import ProductFilter
from django.shortcuts import render,redirect
from login.models import Store
from login.views import upload,handleImageUpload
from login.forms import ImageStoreForm

@login_required
def myStorePage(request):
    list_category = Categories.objects.all()
    dataStore = Store.objects.filter(users__username=request.user)
    list_product = Product.objects.filter(
        prices__isnull=False, photo_products__isnull=False).values(
        'name', 'slug', 'sex', 'prices__price', 'prices__sale', 'photo_products__name', 'prices__price_total', 'category_id__logo')
    filtered_qs = ProductFilter(request.GET, queryset=list_product).qs
    paginator = Paginator(filtered_qs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
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
        return render(request,'storeInfo.html',{'page_obj': page_obj, 
                                                'pages': range(1, page_obj.paginator.num_pages) ,
                                                'dataStore':dataStore[0] ,'current' : request.user ,
                                                'formImage':formImage,
                                                'list_category': list_category
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

