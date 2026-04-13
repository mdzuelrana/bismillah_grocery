import requests
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from order.models import Order
from .models import Payment
from .serializers import PaymentSerializer


# PAYMENT VALIDATION
class PaymentValidationView(APIView):

    def post(self, request):

        val_id = request.data.get("val_id")

        payload = {
            "val_id": val_id,
            "store_id": settings.SSLCOMMERZ_STORE_ID,
            "store_passwd": settings.SSLCOMMERZ_STORE_PASSWORD,
            "format": "json"
        }

        response = requests.get(settings.SSLCOMMERZ_VALIDATION_URL, params=payload)
        data = response.json()

        return Response(data)


# PAYMENT HISTORY
from datetime import timedelta
from django.utils.timezone import now

class PaymentHistoryView(generics.ListAPIView):

    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        user = self.request.user
        days = self.request.query_params.get("days")

        queryset = Payment.objects.filter(user=user)

        # ✅ Filter last N days
        if days:
            try:
                days = int(days)
                date_from = now() - timedelta(days=days)
                queryset = queryset.filter(created_at__gte=date_from)
            except:
                pass

        return queryset.order_by("-created_at")


# PAYMENT SUCCESS


class PaymentSuccessView(APIView):

    def post(self, request):

        tran_id = request.data.get("tran_id")

        payment = Payment.objects.filter(transaction_id=tran_id).first()

        if payment:

            payment.status = "completed"
            payment.save()

            order = payment.order
            order.payment_status = "paid"
            order.is_paid = True
            order.save()

        # ✅ REDIRECT TO FRONTEND PAGE
            return redirect(f"{settings.FRONTEND_URL}/customer-dashboard/payment-success")
        return redirect(f"{settings.FRONTEND_URL}/customer-dashboard")


# PAYMENT FAIL
class PaymentFailView(APIView):

    def post(self, request):

        tran_id = request.data.get("tran_id")

        payment = Payment.objects.filter(transaction_id=tran_id).first()

        if payment:
            payment.status = "failed"
            payment.save()

        return redirect(f"{settings.FRONTEND_URL}/customer-dashboard/orders")


# PAYMENT CANCEL
class PaymentCancelView(APIView):

    def post(self, request):
        return redirect(f"{settings.FRONTEND_URL}/customer-dashboard/cart")


# INITIATE PAYMENT
class SSLCommerzPaymentView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):

        try:
            order = Order.objects.get(id=order_id, customer=request.user)

            tran_id = f"txn_{order.id}"

            data = {

                "store_id": settings.SSLCOMMERZ_STORE_ID,
                "store_passwd": settings.SSLCOMMERZ_STORE_PASSWORD,

                "total_amount": float(order.total_amount),
                "currency": "BDT",
                "tran_id": tran_id,

                "success_url": f"{settings.BASE_URL}/api/payment/success/",
                "fail_url": f"{settings.BASE_URL}/api/payment/fail/",
                "cancel_url": f"{settings.BASE_URL}/api/payment/cancel/",

                "cus_name": request.user.first_name,
                "cus_email": request.user.email,
                "cus_add1": "Dhaka",
                "cus_phone": "01700000000",

                "product_name": "Grocery Order",
                "product_category": "Grocery",
                "product_profile": "general",

                "shipping_method": "NO",
            }

            response = requests.post(settings.SSLCOMMERZ_INIT_URL, data=data)
            result = response.json()

            if result.get("status") == "SUCCESS":

                Payment.objects.create(
                    user=request.user,
                    order=order,
                    transaction_id=tran_id,
                    amount=order.total_amount,
                    status="pending"
                )

                return Response({
                    "payment_url": result["GatewayPageURL"]
                })

            return Response({"error": "Payment initialization failed"})

        except Order.DoesNotExist:
            return Response({"error": "Order not found"})