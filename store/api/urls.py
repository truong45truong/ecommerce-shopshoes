from django.urls import path
from .views import Storeviewset
store = Storeviewset.as_view({
    'get' : 'get_store',
    'post' : 'post_store'
})

urlpatterns = [
    path('store/',store,name="store_logs")
]