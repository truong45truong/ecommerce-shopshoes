from django.urls import path
from . import views

urlpatterns = [
    path('info',views.myStorePage,name='mystore'),
    path('<slug:slugstore>',views.detailStorePage,name='detailstore'),
]