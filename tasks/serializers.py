from rest_framework import serializers
from tasks.models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    image_url        = serializers.SerializerMethodField()
    category_name    = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model  = Product
        fields = [
            'id',
            'seller',
            'category',
            'category_name',  # ✅ readable name for frontend
            'name',
            'description',
            'price',
            'stock',
            'image',          # ✅ for upload (write)
            'image_url',      # ✅ full Supabase URL (read)
            'created_at',
        ]
        read_only_fields = ['seller', 'created_at', 'image_url', 'category_name']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None