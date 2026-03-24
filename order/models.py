from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from tasks.models import Product
# Create your models here.



User = get_user_model()

class Order(models.Model):

    PAYMENT_STATUS = (
        ('pending','Pending'),
        ('paid','Paid'),
        ('failed','Failed')
    )

    customer = models.ForeignKey(User,on_delete=models.CASCADE)

    total_amount = models.DecimalField(max_digits=10,decimal_places=2)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='pending'
    )

    is_paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}"



class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
