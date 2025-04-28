from django.urls import path
from .views_frontend import product_list_view

urlpatterns = [
    path('', product_list_view, name='store-front'),
]
