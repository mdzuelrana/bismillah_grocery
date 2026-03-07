from django.shortcuts import render
from rest_framework import viewsets, permissions
from django.core.mail import send_mail
from django.conf import settings

from tasks.models import Product,Category
from tasks.serializers import ProductSerializer,CategorySerializer
from tasks.permissions import IsReviewOwner,IsSellerOrAdmin
# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user = self.request.user

        # If user not logged in
        if not user.is_authenticated:
            return Product.objects.all()

        if user.role == 'admin':
            return Product.objects.all()

        if user.role == 'seller':
            return Product.objects.filter(seller=user)

        return Product.objects.all()

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)