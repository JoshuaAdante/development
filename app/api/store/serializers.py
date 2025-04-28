from rest_framework import serializers
from .models import Product, Cart, CartItem, Checkout

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'inventory']

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'checked_out', 'items']

class CheckoutSerializer(serializers.ModelSerializer):
    cart = CartSerializer(read_only=True)
    class Meta:
        model = Checkout
        fields = ['id', 'cart', 'name', 'email', 'address', 'total', 'created_at']
