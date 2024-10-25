from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import BasePermission

from orders.models import Order


class IsPaymentByUser(BasePermission):
    """
    check if payment belongs to buyer or admin
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated is True

    def has_object_permission(self, request, view, obj):
        return obj.order.buyer == request.user or request.user.is_staff


class IsPaymentPending(BasePermission):
    """
    check if the status of payment is pending or completed before updating/deleting instance
    """

    message = _('updating or deleting complete payment is not allowed.')

    def has_object_permission(self, request, view, obj):
        if view.action in ('retrieve',):
            return True
        return obj.status == 'P'


class IsPaymentForOrderNotCompleted(BasePermission):
    """
    check if the status of payment for order is completed or not
    """

    message = _('creating a checkout session for completed payment is not allowed.')

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            order_id = view.kwargs.get('order_id')
            order = get_object_or_404(Order, id=order_id)
            return order.status != 'C'

        return False


class DoesOrderHaveAddress(BasePermission):
    """
    check if order has billing and shipping address.
    """

    message = _(
        'creating a checkout session without having a shipping or billing address is not allowed.'
    )

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            order_id = view.kwargs.get('order_id')
            order = get_object_or_404(Order, id=order_id)
            return order.shipping_address and order.billing_address
        return False


class IsOrderPendingWhenCheckOut(BasePermission):
    """
    check the status of the order is pending or completed before updating instance
    """

    message = _('updating closed order is not allowed.')

    def has_object_permission(self, request, view, obj):
        if request.method in ('GET',):
            return True
        return obj.status == 'P'
