from django.urls import path,include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'order',views.OrderViewset)
router.register(r'detailorder',views.DetailOrderViewset)

urlpatterns = [
    path('',include((router.urls))),
]