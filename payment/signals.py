from django.dispatch import receiver
from paypal.standard.ipn.signals import valid_ipn_received,invalid_ipn_received
from order.models import Order
from payment.models import Payment
import datetime
@receiver(valid_ipn_received)
def valid_ipn_signal(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == 'Completed':
        payment = Payment.objects.get(id = ipn_obj.invoice)
        payment.allowed = True
        payment.date_pay = datetime.datetime.now()
        payment.save()
        

@receiver(invalid_ipn_received)
def invalid_ipn_signal(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == 'Completed':
        print("invalid",ipn_obj.invoice)