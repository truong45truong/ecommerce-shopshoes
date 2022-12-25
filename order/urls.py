from django.urls import path,re_path,include
from . import views

urlpatterns = [
    path('shoppingcart',views.shoppingCartPage,name="shoppingcart"),
    path('api/',include('order.api.urls')),
    path('addtocart',views.add_to_cart),
    path('removetocart',views.remove_to_cart,name="removetocart"),
    path('purchase/<str:order_name>/',views.ViewOrder,name="vieworder")
]