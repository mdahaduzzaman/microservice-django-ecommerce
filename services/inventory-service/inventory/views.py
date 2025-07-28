from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from inventory.models import Inventory, InventoryHistory
from inventory.serializers import (
    AddStockSerializer,
    InventorySerializer,
    InventoryHistorySerializer,
)


class InventoryViewSet(ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    lookup_field = "product_id"

    def perform_create(self, serializer):
        instance: Inventory = serializer.save()

        instance.insert_stock(
            quantity=instance.quantity, note="Initial inventory creation"
        )

    @action(
        detail=True,
        methods=["post"],
        serializer_class=AddStockSerializer,
        url_path="add-stock",
    )
    def add_stock(self, request, product_id=None):
        inventory: Inventory = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quantity = serializer.validated_data["quantity"]
        note = serializer.validated_data["note"]
        if quantity > 0:
            inventory.insert_stock(quantity, note=note)
            return Response({"detail": "Stock added."})
        return Response({"detail": "Invalid quantity."}, status=400)

    @action(
        detail=True,
        methods=["post"],
        serializer_class=AddStockSerializer,
        url_path="remove-stock",
    )
    def remove_stock(self, request, product_id=None):
        inventory = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quantity = serializer.validated_data["quantity"]
        note = serializer.validated_data["note"]
        try:
            if quantity > 0:
                inventory.remove_stock(quantity, note=note)
                return Response({"detail": "Stock removed."})
        except ValueError as e:
            return Response({"detail": str(e)}, status=400)
        return Response({"detail": "Invalid quantity."}, status=400)


class InventoryHistoryViewSet(ModelViewSet):
    queryset = InventoryHistory.objects.all()
    serializer_class = InventoryHistorySerializer
