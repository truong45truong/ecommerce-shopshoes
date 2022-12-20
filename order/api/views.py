from rest_framework import viewsets
from order.models import Order,Detail_order
from .serializers import OrderSerializer,DetailOrderSerializer

class OrderViewset(viewsets.ModelViewSet):
    queryset =  Order.objects.all()
    serializer_class = OrderSerializer

class DetailOrderViewset(viewsets.ModelViewSet):
    queryset = Detail_order.objects.all()
    serializer_class = DetailOrderSerializer