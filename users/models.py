from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('seller', 'Seller'),
        ('customer', 'Customer'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    email_verified = models.BooleanField(default=False)
    shopping_preferences = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username
