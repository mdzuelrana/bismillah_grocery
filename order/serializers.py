from rest_framework import serializers
from order.models import Order, OrderItem
from cart.models import CartItem
from django.db import transaction


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'total_amount', 'is_paid', 'items']
        read_only_fields = ['customer', 'total_amount', 'is_paid']

    @transaction.atomic
    def create(self, validated_data):

        user = self.context['request'].user
        cart_items = CartItem.objects.filter(cart__user=user)

        if not cart_items.exists():
            raise serializers.ValidationError("Cart is empty")

        total = 0

        for item in cart_items:
            if item.product.stock < item.quantity:
                raise serializers.ValidationError(
                    f"Not enough stock for {item.product.name}"
                )
            total += item.product.price * item.quantity

        if user.balance < total:
            raise serializers.ValidationError("Insufficient balance")

        
        user.balance -= total
        user.save()

        
        order = Order.objects.create(
            customer=user,
            total_amount=total,
            is_paid=True
        )

        
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity
            )

            
            item.product.stock -= item.quantity
            item.product.save()

        
        cart_items.delete()

        return order
