from django.db import models


class InventoryStatus(models.TextChoices):
    IN_STOCK = "in_stock", "In Stock"
    OUT_OF_STOCK = "out_of_stock", "Out of Stock"
    LOW_STOCK = "low_stock", "Low Stock"


class TransactionType(models.TextChoices):
    ADD = "add", "Add"
    REMOVE = "remove", "Remove"
