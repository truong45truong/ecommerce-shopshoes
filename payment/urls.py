from django.urls import path


from . import views

urlpatterns = [
    path('',views.paymentPage,name='payment'),
    path('paypal-return',views.paypal_return , name="paypal-return"),
    path('paypal-reverse"',views.paypal_reverse , name="paypal-reverse"),
    path('paypal-cancel',views.paypal_cancel , name="paypal-cancel")
]