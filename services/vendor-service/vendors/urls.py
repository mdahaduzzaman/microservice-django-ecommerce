from django.urls import path

from vendors.views import (
    HealthView,
    VendorMeView,
)


urlpatterns = [
    path("health/", HealthView.as_view()),
    path("vendors/me/", VendorMeView.as_view(), name="vendors_me"),
]
