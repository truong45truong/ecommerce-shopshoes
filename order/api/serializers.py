from order.models import Order, Detail_order
from product.models import Product
from rest_framework import serializers
from product.api.serializers import ProductSerializer
class DetailOrderSerializer(serializers.ModelSerializer):
    product_id__name = serializers.CharField()
    product_id__photo_products__name = serializers.CharField()
    product_id__slug = serializers.CharField()
    product_id__prices__price = serializers.FloatField()
    product_id__prices__price_total = serializers.FloatField()
    product_id__prices__sale = serializers.IntegerField()
    class Meta:
        model = Detail_order
        fields = ['product_id__slug','product_id__name','quantity','size','product_id__photo_products__name','product_id__prices__price',
                  'product_id__prices__sale', 'product_id__prices__price_total'
                  ]
    def create(self, validated_data):
        detail_order = Detail_order.objects.create(**validated_data)
        return detail_order
class OrderSerializer(serializers.ModelSerializer):
    detailorders = DetailOrderSerializer(many=True)
    class Meta:
        model = Order
        fields = [
            'name','datetime',
            'receiver','address_receiver',
            'phone_receiver','status',
            'total_price','customer_id',
            'transport_id','detailorders',
        ]