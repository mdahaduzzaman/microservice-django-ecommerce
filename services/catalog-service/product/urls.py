from django.urls import include, path
from rest_framework.routers import DefaultRouter

from product.views import CategoryViewSet, ProductViewSet, HealthView

router = DefaultRouter()

router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"products", ProductViewSet, basename="product")

urlpatterns = [
    path("health/", HealthView.as_view()),
    path("", include(router.urls)),
]
