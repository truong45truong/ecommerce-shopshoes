from django.forms import ModelForm,Form
from django import forms
class PaymentForm(Form):
    order_id = forms.CharField(max_length=50, blank=True, null=True)
    money = forms.IntegerField()
    note = forms.Textarea()
    