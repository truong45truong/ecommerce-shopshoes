from rest_framework.serializers import ModelSerializer
from product.models import Product, Price, Size,Photo_product,Categories

class SizesSerializer(ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'
    def create(self, validated_data):
        size =Size.objects.create( **validated_data)
        return size
class PriceSerializer(ModelSerializer):
    class Meta:
        model = Price
        fields = ['price','sale','datetime_create']
    def create(self, validated_data):
        price =Price.objects.create( **validated_data)
        return price
class PhotoProductSerializer(ModelSerializer):
    class Meta:
        model = Photo_product
        fields = '__all__'
class ProductSerializer(ModelSerializer):
    prices = PriceSerializer(many=True)
    sizes = SizesSerializer(many=True)
    photo_products = PhotoProductSerializer(many=True)
    class Meta:
        model = Product
        fields = ['slug','name','sex','description','store_id','category_id','prices','sizes','photo_products']
    def create(self, validated_data):
        sizes=validated_data.pop('sizes')
        prices_data =validated_data.pop('prices')
        product= Product.objects.create(**validated_data)
        Price.objects.create(product_id=product, **prices_data[0])
        for size in sizes:
            Size.objects.create(product_id=product,**size)
        return product
class CategorySerializer(ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'