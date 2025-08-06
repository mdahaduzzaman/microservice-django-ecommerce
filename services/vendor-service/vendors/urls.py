from django.urls import path, include
from rest_framework.routers import SimpleRouter

from vendors.views import (
    HealthView,
    VendorMeView,
    SubscriptionPlanView,
    VendorPlanView,
    CreateVendorCheckoutView,
)

router = SimpleRouter()
router.register(
    r"subscription-plans", SubscriptionPlanView, basename="subscription-plans"
)

urlpatterns = [
    path("health/", HealthView.as_view()),
    path("vendor-plans/<uuid:vendor>/", VendorPlanView.as_view(), name="vendor_plans"),
    path("me/", VendorMeView.as_view(), name="vendors_me"),
    path("checkout/", CreateVendorCheckoutView.as_view(), name="vendor_checkout"),
    path("", include(router.urls)),
]
