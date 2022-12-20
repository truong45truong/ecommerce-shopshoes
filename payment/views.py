from django.shortcuts import render


def paymentPage (request):
    return render(request,'payment.html')
