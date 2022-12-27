from django.dispatch import receiver
from paypal.standard.ipn.signals import valid_ipn_received,invalid_ipn_received
from order.models import Order

@receiver(valid_ipn_received)
def valid_ipn_signal(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == 'Completed':
        print("valid",ipn_obj.invoice)

@receiver(invalid_ipn_received)
def invalid_ipn_signal(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == 'Completed':
        print("invalid",ipn_obj.invoice)