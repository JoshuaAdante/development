from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Product, Cart, CartItem, Checkout
from .serializers import ProductSerializer, CartSerializer, CartItemSerializer, CheckoutSerializer
from django.db import transaction

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class AddToCartView(APIView):
    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)
        if product.inventory < quantity:
            return Response({'error': 'Insufficient stock'}, status=status.HTTP_400_BAD_REQUEST)
        cart, created = Cart.objects.get_or_create(user=request.user, checked_out=False)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity += quantity
        cart_item.save()
        return Response({'message': 'Added to cart'}, status=status.HTTP_200_OK)

class CartView(APIView):
    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user, checked_out=False)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

class CheckoutView(APIView):
    @transaction.atomic
    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user, checked_out=False)
        items = cart.items.all()
        if not items:
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
        for item in items:
            if item.product.inventory < item.quantity:
                return Response({'error': f'Insufficient stock for {item.product.name}'}, status=status.HTTP_400_BAD_REQUEST)
        total = sum([item.get_total_price() for item in items])
        for item in items:
            item.product.inventory -= item.quantity
            item.product.save()
        cart.checked_out = True
        cart.save()
        checkout = Checkout.objects.create(
            cart=cart,
            name=request.data['name'],
            email=request.data['email'],
            address=request.data['address'],
            total=total
        )
        serializer = CheckoutSerializer(checkout)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
