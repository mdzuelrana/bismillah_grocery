from django.contrib import admin
from order.models import Order, OrderItem

# Register your models here.



class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer',
        'total_amount',
        'is_paid',
        'created_at'
    )
    list_filter = ('is_paid', 'created_at')
    search_fields = ('customer__username',)
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity')
