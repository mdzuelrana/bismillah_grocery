from django.contrib import admin
from review.models import Review

# Register your models here.



@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'product',
        'rating',
        
    )
    list_filter = ('rating',)
    search_fields = ('product__name', 'user__username')
