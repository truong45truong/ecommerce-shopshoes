from django.urls import path,include
from .views import Userviewset
user = Userviewset.as_view({
    'get' : 'get_user',
    'post' : 'post_user'
})
urlpatterns = [
    path('user/',user,name="user_logs")
]
