import uuid
from django.db import models
from django.core.validators import MinValueValidator

from inventory.choices import InventoryStatus, TransactionType


class Inventory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_id = models.UUIDField(unique=True)  # Id from product service
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    low_stock_threshold = models.IntegerField(default=10)
    status = models.CharField(
        max_length=20, choices=InventoryStatus.choices, default=InventoryStatus.IN_STOCK
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "inventory"
        ordering = ["-last_restocked"]

    def update_status(self):
        if self.quantity <= 0:
            self.status = InventoryStatus.OUT_OF_STOCK
        elif self.quantity <= self.low_stock_threshold:
            self.status = InventoryStatus.LOW_STOCK
        else:
            self.status = InventoryStatus.IN_STOCK

    def insert_stock(self, quantity, note: str = None):
        previous = self.quantity
        self.quantity += quantity
        self.save()
        InventoryHistory.objects.create(
            inventory=self,
            previous_quantity=previous,
            change_quantity=quantity,
            current_quantity=self.quantity,
            transaction_type=TransactionType.ADD,
            note=note,
        )

    def remove_stock(self, quantity, note: str = None):
        if quantity > self.quantity:
            raise ValueError("Cannot remove more stock than available")
        previous = self.quantity
        self.quantity -= quantity
        self.save()
        InventoryHistory.objects.create(
            inventory=self,
            previous_quantity=previous,
            change_quantity=quantity,
            current_quantity=self.quantity,
            transaction_type=TransactionType.REMOVE,
            note=note,
        )

    def save(self, *args, **kwargs):
        self.update_status()
        super().save(*args, **kwargs)


class InventoryHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    inventory = models.ForeignKey(
        Inventory, on_delete=models.CASCADE, related_name="inventory"
    )
    previous_quantity = models.PositiveIntegerField()
    change_quantity = models.IntegerField()
    current_quantity = models.PositiveIntegerField()
    transaction_type = models.CharField(max_length=10, choices=TransactionType.choices)
    note = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "inventory_history"
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["inventory"]),
            models.Index(fields=["transaction_type"]),
        ]

    def __str__(self):
        return f"{self.transaction_type} of {self.change_quantity} at {self.timestamp}"
