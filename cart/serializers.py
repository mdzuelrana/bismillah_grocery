from rest_framework import serializers
from cart.models import CartItem, Wishlist,Cart
from tasks.models import Product





class CartItemSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(source="product.name", read_only=True)
    product_price = serializers.DecimalField(source="product.price", max_digits=10, decimal_places=2, read_only=True)
    #product_image = serializers.ImageField(source="product.image", read_only=True)

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "product_name",
            "product_price",
            # "product_image",
            "quantity"
        ]

    def create(self, validated_data):
        user = self.context["request"].user

        cart, created = Cart.objects.get_or_create(user=user)

        product = validated_data["product"]
        quantity = validated_data.get("quantity", 1)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return cart_item




class WishlistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wishlist
        fields = ['id', 'product']
        read_only_fields = ['id']

    def create(self, validated_data):
        user = self.context['request'].user
        product = validated_data['product']

        wishlist_item, created = Wishlist.objects.get_or_create(
            user=user,
            product=product
        )

        return wishlist_item
