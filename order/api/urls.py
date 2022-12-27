from django.urls import path,include
from .views import  DetailOrderViewset


detail_order = DetailOrderViewset.as_view({
    'get' : 'get_detail_order',
})

urlpatterns = [
    path('detail-order/',detail_order,name="get_detail_order")
]