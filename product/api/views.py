from rest_framework.decorators import  api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from product.models import Product, Size, Price
from .serializers import PriceSerializer, ProductSerializer, SizesSerializer

class Productviewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Price.objects.all()

    @action(method=["GET"],detail=False,url_path="product",url_name="get_product")
    def get_product(self, request,*args, **kwargs):
        slug=request.GET.get('slug')
        store = request.GET.get('store')
        if slug :
            queryset = Product.objects.filter(slug=slug)
        if store :
            queryset = Product.objects.filter(store_id=request.user.store_id)
        else:
            queryset = Product.objects.all()
        serializer = ProductSerializer(queryset,many=True)
        return Response(serializer.data)
    
    
class Priceviewset(viewsets.ModelViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
class Sizeviewset(viewsets.ModelViewSet):
    queryset = Size.objects.all()
    serializer_class = SizesSerializer
