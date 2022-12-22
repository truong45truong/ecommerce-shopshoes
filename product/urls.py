from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path('<slug:slug>/',views.productPage,name='product'),
    path('productdetail/<slug:slug>/',views.productDetail,name='productdetail'),
    path('productnew/',views.productNewPage,name='productnew'),
]