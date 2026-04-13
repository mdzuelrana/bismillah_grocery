from django.shortcuts import render
from rest_framework import viewsets, permissions
from order.models import Order
from order.serializers import OrderSerializer
from django.core.mail import send_mail
from users.permissions import IsAdminUserRole
from django.conf import settings


class AdminOrderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset           = Order.objects.all().prefetch_related('items__product')
    serializer_class   = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUserRole]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class   = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(
            customer=self.request.user
        ).prefetch_related('items__product').order_by('-created_at')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request  # ✅ lets serializer build full image URLs
        return context

    def perform_create(self, serializer):
        order = serializer.save(customer=self.request.user)

        send_mail(
            subject=f"Order Confirmed — #{order.id}",
            message=(
                f"Hi {order.full_name},\n\n"
                f"Your order #{order.id} has been placed successfully.\n"
                f"Total: ৳ {order.total_amount}\n\n"
                f"We'll notify you once it's shipped.\n\n"
                f"Thank you for shopping with us!"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.request.user.email],
            fail_silently=True,
        )


class SellerOrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class   = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request  # ✅ same fix for seller view
        return context

    def get_queryset(self):
        user = self.request.user
        if user.role == 'seller':
            return Order.objects.filter(
                items__product__seller=user
            ).distinct().prefetch_related('items__product')
        return Order.objects.none()