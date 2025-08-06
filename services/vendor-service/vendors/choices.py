from django.db import models


class BillingCycle(models.TextChoices):
    MONTHLY = "monthly", "Monthly"
    YEARLY = "yearly", "Yearly"


class Status(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"
    CANCELLED = "cancelled", "Cancelled"
    EXPIRED = "expired", "Expired"
