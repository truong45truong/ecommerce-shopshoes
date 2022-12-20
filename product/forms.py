from dataclasses import fields
from secrets import choice
from django.forms import ModelForm
from .models import Product, Photo_product, Price, Size
from django import forms

class ProductForm(ModelForm):
    CHOICE=(
        ("0","All"),
        ("1","Men"),
        ("2","Women")
    )
    gender = forms.ChoiceField(choices=CHOICE)
    class Meta:
        model = Product
        fields = ['name','gender','category_id','description']
class PhotoProductForm(ModelForm):
    class Meta:
        model =Photo_product
        fields =['data']
class PriceForm(ModelForm):
    class Meta:
        model = Price
        fields = ['price','sale']