from rest_framework import serializers
from order.models import Order, OrderItem
from cart.models import CartItem
from django.db import transaction


class OrderItemSerializer(serializers.ModelSerializer):
    product_name  = serializers.CharField(source='product.name',  read_only=True)
    product_image = serializers.ImageField(source='product.image', read_only=True)

    class Meta:
        model  = OrderItem
        fields = ['id', 'product', 'product_name', 'product_image', 'quantity', 'price']


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
            'city',           # ✅ added
            'notes',          # ✅ added
            'order_status',   # ✅ added
            'payment_status', # ✅ added
            'created_at',     # ✅ added — needed for Orders page date display
        ]
        read_only_fields = ['customer', 'total_amount', 'is_paid', 'order_status', 'payment_status']

    @transaction.atomic
    def create(self, validated_data):
        user       = self.context['request'].user
        cart_items = CartItem.objects.filter(cart__user=user).select_related('product')

        if not cart_items.exists():
            raise serializers.ValidationError("Your cart is empty.")

        # ── stock check ───────────────────────────────────────────────────────
        for item in cart_items:
            if item.product.stock < item.quantity:
                raise serializers.ValidationError(
                    f"Not enough stock for '{item.product.name}'. "
                    f"Available: {item.product.stock}, Requested: {item.quantity}"
                )

        # ── calculate total ───────────────────────────────────────────────────
        total = sum(item.product.price * item.quantity for item in cart_items)

        # ── create order ──────────────────────────────────────────────────────
        order = Order.objects.create(
            customer       = user,
            total_amount   = total,
            payment_status = "pending",
            order_status   = "processing",
            is_paid        = False,
            full_name      = validated_data.get("full_name"),
            phone          = validated_data.get("phone"),
            address        = validated_data.get("address"),
            city           = validated_data.get("city", ""),   # ✅ added
            notes          = validated_data.get("notes", ""),  # ✅ added
        )

        # ── create order items ────────────────────────────────────────────────
        for item in cart_items:
            OrderItem.objects.create(
                order    = order,
                product  = item.product,
                quantity = item.quantity,
                price    = item.product.price,  # ✅ THE FIX — this was missing, causing 500
            )

        # ── clear cart after order placed ─────────────────────────────────────
        cart_items.delete()  # ✅ empty the cart once order is created

        return order