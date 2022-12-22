from rest_framework.serializers import ModelSerializer
from payment.models import Order,Payment

class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = '__adll__'
    def create(self, validated_data):
        payment = Payment.objects.create(**validated_data)
        return payment
    