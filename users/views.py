from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
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
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from rest_framework.decorators import api_view


# Create your views here.


@api_view(['POST'])
def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError):
        return Response({"detail": "Invalid activation link."}, status=400)

    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return Response({"detail": "Account activated successfully."})
    return Response({"detail": "Activation link invalid or expired."}, status=400)


@api_view(['POST'])
def register_user(request):
    user = User.objects.create_user(
        username=request.data["username"],
        email=request.data["email"],
        password=request.data["password"],
        is_active=False,
    )
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    send_activation_email(user, uid, token)
    return Response({"detail": "Check your email to activate your account."}, status=201)

class AdminDashboardStats(APIView):
    permission_classes = [IsAuthenticated, IsAdminUserRole]

    def get(self, request):
        total_users    = User.objects.count()
        total_products = Product.objects.count()
        total_orders   = Order.objects.count()

        # ✅ only count revenue from paid orders
        total_revenue = Order.objects.filter(
            payment_status="paid"
        ).aggregate(total=Sum('total_amount'))['total'] or 0

        # ✅ order status breakdown
        return Response({
            "total_users":    total_users,
            "total_products": total_products,
            "total_orders":   total_orders,
            "total_revenue":  total_revenue,
            "processing":     Order.objects.filter(order_status="processing").count(),
            "confirmed":      Order.objects.filter(order_status="confirmed").count(),
            "shipped":        Order.objects.filter(order_status="shipped").count(),
            "delivered":      Order.objects.filter(order_status="delivered").count(),
            "cancelled":      Order.objects.filter(order_status="cancelled").count(),
        })


class AdminProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]


class ProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user

        return Response({
            "username": user.username,
            "email": user.email
        })

    def patch(self, request):

        user = request.user

        username = request.data.get("username")
        password = request.data.get("password")

        if username:
            user.username = username

        if password:
            user.set_password(password)

        user.save()

        return Response({"message": "Profile updated"})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def deposit(self, request):
        amount = float(request.data.get('amount'))
        request.user.balance += amount
        request.user.save()
        return Response({"balance": request.user.balance})
