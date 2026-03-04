from django.db import models
from django.contrib.auth import get_user_model
from order.models import Order

# Create your models here.


User = get_user_model()
    
    
class Payment(models.Model):

    STATUS_CHOICES = (
        ('pending','Pending'),
        ('completed','Completed'),
        ('failed','Failed')
    )

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)

    transaction_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10,decimal_places=2)

    status = models.CharField(max_length=20,choices=STATUS_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_id