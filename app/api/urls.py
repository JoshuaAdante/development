from django.urls import path, include
from .views import HelloWorld
from .views import Students
from .views import ContactListView

urlpatterns = [
    path('hello/', HelloWorld.as_view(), name='hello_world'),
    path('students/', Students.as_view(), name='list_students'),
    path('contact/', ContactListView.as_view(), name='contact_new'),
    path('store/', include('api.store.urls')),
    path('store/front/', include('api.store.urls_frontend')),
]
