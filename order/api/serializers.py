from order.models import Order, Detail_order
from product.models import Product
from rest_framework import serializers

class DetailOrderSerializer(serializers.ModelSerializer):
    status = serializers.BooleanField()
    quantity = serializers.IntegerField()

    class Meta:
        model = Detail_order
        fields = ['product_id','status','quantity']
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