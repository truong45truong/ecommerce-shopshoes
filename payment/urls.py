from django.urls import path


from . import views

urlpatterns = [
    path('',views.paymentPage,name='payment'),
    path('paypal-return',views.paypal_return , name="paypal-return"),
    path('payment/paypal-reverse"',views.paypal_reverse , name="paypal-reverse"),
    path('payment/paypal-cancel',views.paypal_cancel , name="paypal-cancel"),
    path('qrcode/<str:token>/',views.qrcodePage,name='qrcode'),
    path('payonreceipt',views.payOnReceipt),
    path('removepayment',views.removePayment)
    
]