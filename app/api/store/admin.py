from django.contrib import admin
from .models import Product, Cart, CartItem, Checkout

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Checkout)
