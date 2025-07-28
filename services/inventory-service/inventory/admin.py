from django.contrib import admin

from inventory.models import Inventory, InventoryHistory


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ("product_id", "quantity", "low_stock_threshold", "status")
    search_fields = ("product_id", "status")


@admin.register(InventoryHistory)
class InventoryHistoryAdmin(admin.ModelAdmin):
    list_display = [
        "inventory",
        "previous_quantity",
        "change_quantity",
        "current_quantity",
        "transaction_type",
    ]
    search_fields = ("inventory__product_id", "transaction_type")
