from django.urls import path, include
from rest_framework.routers import DefaultRouter

from payments.views import PaymentMethodViewSet, CheckoutSessionView

router = DefaultRouter()
router.register(r"payment-methods", PaymentMethodViewSet, basename="payment-methods")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "create-checkout-session/",
        CheckoutSessionView.as_view(),
        name="create-checkout-session",
    ),
]
