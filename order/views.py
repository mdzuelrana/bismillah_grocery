from django.shortcuts import render
from order.models import Order
from order.serializers import OrderSerializer
from django.core.mail import send_mail
from users.permissions import IsAdminUserRole
from django.conf import settings
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

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


class SellerOrderViewSet(viewsets.ModelViewSet):  # ✅ changed from ReadOnlyModelViewSet
    serializer_class   = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        user = self.request.user
        if user.role == 'seller':
            return Order.objects.filter(
                items__product__seller=user
            ).distinct().prefetch_related('items__product').order_by('-created_at')
        return Order.objects.none()

    def partial_update(self, request, *args, **kwargs):
        # ✅ seller can only update order_status
        order = self.get_object()
        order_status = request.data.get('order_status')
        if order_status not in ['confirmed', 'shipped', 'delivered', 'cancelled']:
            return Response(
                {"error": "Invalid status."},
                status=status.HTTP_400_BAD_REQUEST
            )
        order.order_status = order_status
        order.save()
        return Response(OrderSerializer(order, context={'request': request}).data)