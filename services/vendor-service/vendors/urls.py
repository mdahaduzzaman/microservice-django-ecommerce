from django.urls import path, include
from rest_framework.routers import DefaultRouter

from vendors.views import VendorViewSet, HealthView

router = DefaultRouter()

router.register('vendors', VendorViewSet, basename="vendors")

urlpatterns = [
    path("", include(router.urls)),
    path("health", HealthView.as_view()),
]
