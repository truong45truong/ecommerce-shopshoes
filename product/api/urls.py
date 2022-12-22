from django.urls import path,include
from .views import Productviewset,CategoryViewset
product = Productviewset.as_view({
    'get' : 'get_product',
    #'post' : 'post_product'
})
category = CategoryViewset.as_view({
    'get' : 'get_category',
})
urlpatterns = [
    path('product/',product,name="get_product"),
    path('category/',category,name="get_category"),
]