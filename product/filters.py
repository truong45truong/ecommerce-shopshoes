import django_filters
from .models import Product
class ProductFilter(django_filters.FilterSet):
    price = django_filters.NumberFilter()
    price__gt = django_filters.NumberFilter(field_name='price',lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='price',lookup_expr='lt')
    def price_total(price_current,sale):
        return ((100-sale)*price_current)/100
    class Meta:
        model = Product
        # Declare all your model fields by which you will filter
        # your queryset here:
        fields = ['price']