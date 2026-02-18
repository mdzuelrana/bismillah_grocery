from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.models import User
from rest_framework.views import APIView
from .serializers import ProfileSerializer
from users.permissions import IsAdminUserRole
from tasks.models import Product
from tasks.serializers import ProductSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from tasks.models import Product
from users.models import User
from order.models import Order
# Create your views here.





class AdminDashboardStats(APIView):
    permission_classes = [IsAuthenticated, IsAdminUserRole]

    def get(self, request):
        total_users = User.objects.count()
        total_products = Product.objects.count()
        total_orders = Order.objects.count()
        total_revenue = Order.objects.aggregate(
            total=Sum('total_amount')
        )['total'] or 0

        return Response({
            "total_users": total_users,
            "total_products": total_products,
            "total_orders": total_orders,
            "total_revenue": total_revenue,
        })


class AdminProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = ProfileSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def deposit(self, request):
        amount = float(request.data.get('amount'))
        request.user.balance += amount
        request.user.save()
        return Response({"balance": request.user.balance})
