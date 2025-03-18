import uuid
from django.db import models


class Vendor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)
    address = models.TextField()
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class VendorProfile(models.Model):
    vendor = models.OneToOneField(
        Vendor, on_delete=models.CASCADE, related_name="vendor_profile"
    )
    business_name = models.CharField(max_length=255)
    tax_id = models.CharField(max_length=50, blank=True, null=True)
    bank_account = models.CharField(max_length=50, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class VendorUser(models.Model):
    ROLE_CHOICES = (
        ("owner", "Owner"),  # Full access
        ("manager", "Manager"),  # Can manage products/orders
        ("staff", "Staff"),  # Limited access
    )

    user_id = models.UUIDField()  # User ID from (Auth Service)
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name="vendor_users"
    )
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default="staff"
    )  # A user can have one role per vendor
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user_id", "vendor")

    def __str__(self):
        return f"{self.user_id} ({self.role}) - {self.vendor.name}"
