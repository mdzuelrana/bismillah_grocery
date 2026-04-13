import requests
from django.conf import settings
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny  # ✅ import AllowAny
from rest_framework import generics, status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from datetime import timedelta
from django.utils.timezone import now

from order.models import Order
from .models import Payment
from .serializers import PaymentSerializer


# ── INITIATE PAYMENT ──────────────────────────────────────────────────────────
class SSLCommerzPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, customer=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        Payment.objects.filter(order=order, status="pending").delete()

        tran_id = f"txn_{order.id}"

        data = {
            "store_id":         settings.SSLCOMMERZ_STORE_ID,
            "store_passwd":     settings.SSLCOMMERZ_STORE_PASSWORD,
            "total_amount":     float(order.total_amount),
            "currency":         "BDT",
            "tran_id":          tran_id,
            "success_url":      f"{settings.BASE_URL}/api/payment/success/",
            "fail_url":         f"{settings.BASE_URL}/api/payment/fail/",
            "cancel_url":       f"{settings.BASE_URL}/api/payment/cancel/",
            "cus_name":         request.user.get_full_name() or request.user.username,
            "cus_email":        request.user.email,
            "cus_add1":         order.address or "Bangladesh",
            "cus_phone":        order.phone   or "01700000000",
            "product_name":     "Grocery Order",
            "product_category": "Grocery",
            "product_profile":  "general",
            "shipping_method":  "NO",
        }

        response = requests.post(settings.SSLCOMMERZ_INIT_URL, data=data)
        result   = response.json()

        if result.get("status") == "SUCCESS":
            Payment.objects.create(
                user=request.user,
                order=order,
                transaction_id=tran_id,
                amount=order.total_amount,
                status="pending",
            )
            return Response({"payment_url": result["GatewayPageURL"]})

        return Response(
            {"error": "Payment initialization failed", "details": result},
            status=status.HTTP_502_BAD_GATEWAY,
        )


# ── SUCCESS ───────────────────────────────────────────────────────────────────
from cart.models import CartItem  # ✅ add this import

@method_decorator(csrf_exempt, name="dispatch")
class PaymentSuccessView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        tran_id = request.POST.get("tran_id")
        val_id  = request.POST.get("val_id")

        payment = Payment.objects.filter(transaction_id=tran_id).first()

        if not payment:
            return HttpResponse(_redirect_html(
                f"{settings.FRONTEND_URL}/customer-dashboard/orders?error=payment_not_found"
            ), content_type="text/html")

        if payment.status != "completed":
            payment.status = "completed"
            payment.val_id = val_id
            payment.save()

            order = payment.order
            order.payment_status = "paid"
            order.is_paid        = True
            order.save()

            # ✅ clear cart HERE — only after payment is confirmed
            CartItem.objects.filter(cart__user=order.customer).delete()

        return HttpResponse(_redirect_html(
            
            f"{settings.FRONTEND_URL}/customer-dashboard/payment-success"
            f"?order_id={payment.order.id}"
        ), content_type="text/html")


# ── FAIL ──────────────────────────────────────────────────────────────────────
@method_decorator(csrf_exempt, name="dispatch")
class PaymentFailView(APIView):
    permission_classes = [AllowAny]  # ✅

    def post(self, request):
        tran_id = request.POST.get("tran_id")
        Payment.objects.filter(transaction_id=tran_id, status="pending").update(status="failed")

        return HttpResponse(_redirect_html(
            f"{settings.FRONTEND_URL}/customer-dashboard/orders?payment=failed"
        ), content_type="text/html")


# ── CANCEL ────────────────────────────────────────────────────────────────────
@method_decorator(csrf_exempt, name="dispatch")
class PaymentCancelView(APIView):
    permission_classes = [AllowAny]  # ✅

    def post(self, request):
        tran_id = request.POST.get("tran_id")
        Payment.objects.filter(transaction_id=tran_id, status="pending").update(status="cancelled")

        return HttpResponse(_redirect_html(
            f"{settings.FRONTEND_URL}/customer-dashboard/cart?payment=cancelled"
        ), content_type="text/html")


# ── VALIDATION ────────────────────────────────────────────────────────────────
class PaymentValidationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        val_id  = request.data.get("val_id")
        payload = {
            "val_id":       val_id,
            "store_id":     settings.SSLCOMMERZ_STORE_ID,
            "store_passwd": settings.SSLCOMMERZ_STORE_PASSWORD,
            "format":       "json",
        }
        response = requests.get(settings.SSLCOMMERZ_VALIDATION_URL, params=payload)
        return Response(response.json())


# ── HISTORY ───────────────────────────────────────────────────────────────────
class PaymentHistoryView(generics.ListAPIView):
    serializer_class   = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user     = self.request.user
        days     = self.request.query_params.get("days")
        queryset = Payment.objects.filter(user=user)

        if days:
            try:
                date_from = now() - timedelta(days=int(days))
                queryset  = queryset.filter(created_at__gte=date_from)
            except ValueError:
                pass

        return queryset.order_by("-created_at")


# ── HELPER ────────────────────────────────────────────────────────────────────
def _redirect_html(url: str) -> str:
    return f"""<!DOCTYPE html>
<html>
  <head><meta http-equiv="refresh" content="0;url={url}"></head>
  <body>Redirecting...</body>
</html>"""