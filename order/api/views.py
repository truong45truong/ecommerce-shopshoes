from rest_framework import viewsets
from order.models import Order,Detail_order
from login.models import Customer
from .serializers import OrderSerializer,DetailOrderSerializer
from rest_framework.decorators import  api_view, action
from rest_framework.response import Response

class DetailOrderViewset(viewsets.ModelViewSet):
    queryset = Detail_order.objects.all()
    serializer_class = DetailOrderSerializer
    
    @action(methods=['GET'],detail=False , url_path="detail_order",url_name="detail_order")
    def get_detail_order(self,request,*args, **kwargs):
        customer_slug = request.GET['slug']
        customer = Customer.objects.get(slug = customer_slug)
        queryset = Detail_order.objects.filter(order_id__isnull = True , customer_id = customer,product_id__photo_products__isnull=False).values(
            'product_id__name','quantity','size','product_id__photo_products__name'
        )
        print(queryset.query)
        serializer = DetailOrderSerializer(queryset, many = True)
        return Response(serializer.data)
