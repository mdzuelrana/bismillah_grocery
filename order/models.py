from django.db import models
from django.contrib.auth import get_user_model
from tasks.models import Product

User = get_user_model()


class Order(models.Model):

    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('paid',    'Paid'),
        ('failed',  'Failed'),
    )

    ORDER_STATUS = (
        ('processing', 'Processing'),
        ('confirmed',  'Confirmed'),
        ('shipped',    'Shipped'),
        ('delivered',  'Delivered'),
        ('cancelled',  'Cancelled'),
    )

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
    )

    total_amount    = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    full_name = models.CharField(max_length=255, null=True, blank=True)
    phone     = models.CharField(max_length=20,  null=True, blank=True)
    address   = models.TextField(null=True, blank=True)
    city      = models.CharField(max_length=100, null=True, blank=True)
    notes     = models.TextField(null=True, blank=True)

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='pending',
        db_index=True,
    )
    order_status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS,
        default='processing',
        db_index=True,
    )
    is_paid = models.BooleanField(default=False, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f"Order #{self.id} — {self.customer.email}"

    @property
    def net_amount(self):
        return self.total_amount - self.discount_amount

    @property
    def item_count(self):
        return self.items.count()


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE,
    )
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price    = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return f"{self.quantity}x {self.product.name} (Order #{self.order.id})"

    @property
    def subtotal(self):
        return self.quantity * self.price