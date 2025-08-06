from django.db import models


class Status(models.TextChoices):
    PENDING = "pending", "Pending"
    COMPLETED = "completed", "Completed"
    FAILED = "failed", "Failed"
    REFUNDED = "refunded", "Refunded"
    CANCELLED = "cancelled", "Cancelled"


class TransactionType(models.TextChoices):
    SUBSCRIPTION = "subscription", "Subscription"
    ORDER = "order", "Order"
