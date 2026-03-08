from django.db import models
from django.db import models
from django.conf import settings
from tasks.models import Product
# Create your models here.


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

from rest_framework import serializers
from cart.models import Wishlist


class WishlistSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(source="product.name", read_only=True)
    product_price = serializers.DecimalField(
        source="product.price",
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    #product_image = serializers.ImageField(source="product.image", read_only=True)

    class Meta:
        model = Wishlist
        unique_together = ['user', 'product']

        fields = [
            "id",
            "product",
            "product_name",
            "product_price",
            # "product_image"
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        product = validated_data["product"]

        wishlist_item, created = Wishlist.objects.get_or_create(
            user=user,
            product=product
        )

        return wishlist_item
        
