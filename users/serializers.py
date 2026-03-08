from djoser.serializers import UserCreateSerializer
from users.models import User
from rest_framework import serializers
from .models import User
from order.models import Order
from cart.models import Wishlist

class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id','email','username','password','role')




class ProfileSerializer(serializers.ModelSerializer):

    purchase_history = serializers.SerializerMethodField()
    wishlist = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'role'
            'balance',
            'shopping_preferences',
            'purchase_history',
            'wishlist'
        ]

    def get_purchase_history(self, obj):
        orders = Order.objects.filter(customer=obj)
        return [{"order_id": o.id, "total": o.total_amount} for o in orders]

    def get_wishlist(self, obj):
        wishlist_items = Wishlist.objects.filter(user=obj)
        return [item.product.name for item in wishlist_items]
