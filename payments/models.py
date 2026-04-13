from django.db import models
from django.contrib.auth import get_user_model
from order.models import Order

User = get_user_model()


class Payment(models.Model):

    STATUS_CHOICES = (
        ('pending',   'Pending'),
        ('completed', 'Completed'),
        ('failed',    'Failed'),
        ('cancelled', 'Cancelled'),
    )

    user  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')

    transaction_id = models.CharField(max_length=100, unique=True)
    val_id         = models.CharField(max_length=100, blank=True, null=True)
    amount         = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        db_index=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    def __str__(self):
        return f"{self.transaction_id} | {self.user.email} | {self.status}"