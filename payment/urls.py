from django.urls import include, path
from rest_framework.routers import DefaultRouter

from payment.views import (
    PaymentViewSet,
    CheckoutAPIView,
)


app_name = 'payment'

router = DefaultRouter()
router.register(r'', PaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('checkout/<int:pk>/', CheckoutAPIView.as_view(), name='checkout'),
]
