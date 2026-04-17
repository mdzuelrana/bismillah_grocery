from django.db import models
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    seller   = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name        = models.CharField(max_length=200)
    description = models.TextField()
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    stock       = models.PositiveIntegerField()
    image       = models.ImageField(
        upload_to='products/',
        storage=S3Boto3Storage(),  # ✅ forces Supabase S3
        null=True,
        blank=True
    )
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name