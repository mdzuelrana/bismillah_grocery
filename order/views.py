from django.shortcuts import render
from rest_framework import viewsets,permissions
from order.models import Order
from order.serializers import OrderSerializer
from django.core.mail import send_mail
from users.permissions import IsAdminUserRole
from django.conf import settings
# Create your views here.




class AdminOrderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUserRole]


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)

    def perform_create(self, serializer):
        order = serializer.save(customer=self.request.user)

       
        send_mail(
            subject="Order Confirmation",
            message=f"Your order #{order.id} was successful.\nTotal: {order.total_amount}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.request.user.email],
            fail_silently=True,
        )


class SellerOrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'seller':
            return Order.objects.filter(
                items__product__seller=user
            ).distinct()

        return Order.objects.none()
