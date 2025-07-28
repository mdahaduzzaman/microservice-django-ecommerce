from rest_framework import serializers

from inventory.models import Inventory, InventoryHistory


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = "__all__"


class InventoryHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryHistory
        fields = "__all__"


class AddStockSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1, required=True)
    note = serializers.CharField(max_length=255, required=False, allow_blank=True)

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value
