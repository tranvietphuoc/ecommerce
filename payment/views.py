from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from orders.models import Order
from orders.permissions import IsOrderByBuyerOrAdmin
from payment.models import Payment
from payment.permissions import (
    DoesOrderHaveAddress,
    IsOrderPendingWhenCheckOut,
    IsPaymentByUser,
    IsPaymentForOrderNotCompleted,
    IsPaymentPending,
)

from payment.serializers import CheckoutSerializer, PaymentSerializer
from payment.utils import send_payment_success_email_task


class PaymentViewSet(ModelViewSet):
    """
    CRUD payment for an order
    """

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsPaymentByUser]

    def get_queryset(self):
        res = super().get_queryset()
        user = self.request.user
        return res.filter(order__buyer=user)

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            self.permission_classes += [IsPaymentPending]

        return super().get_permissions()


class CheckoutAPIView(RetrieveUpdateAPIView):
    """
    create, retrieve, update billing address, shipping address and payment of an order

    """

    queryset = Order.objects.all()
    serializer_class = CheckoutSerializer
    permission_classes = [IsOrderByBuyerOrAdmin]

    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH'):
            self.permission_classes += [IsOrderPendingWhenCheckOut]
        return super().get_permissions()
