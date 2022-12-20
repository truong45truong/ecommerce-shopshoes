from django.urls import path,include
from .views import Productviewset
product = Productviewset.as_view({
    'get' : 'get_product',
    #'post' : 'post_product'
})
urlpatterns = [
    path('product/',product,name="get_product")
]
print(urlpatterns)