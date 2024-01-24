from django.urls import path, include

from users.views import PaymentListAPIView

urlpatterns = [
    path('payment/', PaymentListAPIView.as_view(), name='payment_list'),
]
