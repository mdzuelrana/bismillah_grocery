from rest_framework import serializers
from order.models import Order, OrderItem
from cart.models import CartItem
from django.db import transaction


class OrderItemSerializer(serializers.ModelSerializer):
    product_name  = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.SerializerMethodField()

    class Meta:
        model  = OrderItem
        fields = ['id', 'product', 'product_name', 'product_image', 'quantity', 'price']

    def get_product_image(self, obj):
        request = self.context.get('request')
        if obj.product.image and request:
            return request.build_absolute_uri(obj.product.image.url)
        return None


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model  = Order
        fields = [
            'id',
            'customer',
            'total_amount',
            'is_paid',
            'items',
            'full_name',
            'phone',
            'address',
            'city',
            'notes',
            'order_status',
            'payment_status',
            'created_at',
        ]
        read_only_fields = [
            'customer',
            'total_amount',
            'is_paid',
            'order_status',
            'payment_status',
        ]

    @transaction.atomic
    def create(self, validated_data):
        user       = self.context['request'].user
        cart_items = CartItem.objects.filter(cart__user=user).select_related('product')

        if not cart_items.exists():
            raise serializers.ValidationError("Your cart is empty.")

        for item in cart_items:
            if item.product.stock < item.quantity:
                raise serializers.ValidationError(
                    f"Not enough stock for '{item.product.name}'. "
                    f"Available: {item.product.stock}, Requested: {item.quantity}"
                )

        total = sum(item.product.price * item.quantity for item in cart_items)

        order = Order.objects.create(
            customer       = user,
            total_amount   = total,
            payment_status = "pending",
            order_status   = "processing",
            is_paid        = False,
            full_name      = validated_data.get("full_name"),
            phone          = validated_data.get("phone"),
            address        = validated_data.get("address"),
            city           = validated_data.get("city", ""),
            notes          = validated_data.get("notes", ""),
        )

        for item in cart_items:
            OrderItem.objects.create(
                order    = order,
                product  = item.product,
                quantity = item.quantity,
                price    = item.product.price,
            )

        # cart cleared in PaymentSuccessView after payment confirmed
        return order