from django.shortcuts import render
from rest_framework import viewsets
from cart.models import CartItem, Wishlist
from cart.serializers import CartItemSerializer, WishlistSerializer
# Create your views here.


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
