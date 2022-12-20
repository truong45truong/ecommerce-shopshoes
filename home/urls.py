from django.urls import path
from . import views
urlpatterns = [
    path('',views.homePage,name='home'),
    path('info-account',views.myAccountPage,name='myaccount'),
    path('introduce',views.introducePage,name='introduce'),
    path('contact',views.contactPage,name='contact'),
]