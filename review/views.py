from django.shortcuts import render
from rest_framework import viewsets,permissions
from review.models import Review
from review.serializers import ReviewSerializer
from tasks.permissions import IsReviewOwner
from order.models import Order
# Create your views here.


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsReviewOwner]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        product = serializer.validated_data['product']
        user = self.request.user

        # Check if user purchased product
        has_bought = Order.objects.filter(
            customer=user,
            items__product=product,
            is_paid=True
        ).exists()

        if not has_bought:
            raise PermissionError("You cannot review a product you haven't purchased.")

        serializer.save(user=user)

