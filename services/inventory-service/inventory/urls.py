from django.urls import path, include
from rest_framework.routers import SimpleRouter

from inventory.views import InventoryViewSet, InventoryHistoryViewSet

router = SimpleRouter()

router.register(r"inventory", InventoryViewSet, basename="inventory")
router.register(
    r"inventory-history", InventoryHistoryViewSet, basename="inventory-history"
)

urlpatterns = [
    path("", include(router.urls)),
]
