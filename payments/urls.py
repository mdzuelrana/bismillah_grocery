from django.urls import path
from .views import *

urlpatterns = [

    path('pay/<int:order_id>/', SSLCommerzPaymentView.as_view()),

    path('success/', PaymentSuccessView.as_view()),
    path('fail/', PaymentFailView.as_view()),
    path('cancel/', PaymentCancelView.as_view()),

    path('history/', PaymentHistoryView.as_view()),

    path('validate/', PaymentValidationView.as_view()),
]