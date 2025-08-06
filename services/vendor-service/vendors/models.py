import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import UniqueConstraint

from vendors.choices import BillingCycle, Status


class TimeStampedModel(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_("ID")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class SubscriptionPlan(TimeStampedModel):
    name = models.CharField(max_length=100)
    monthly_price = models.FloatField(null=True, blank=True)
    yearly_price = models.FloatField(null=True, blank=True)
    description = models.TextField()
    features = models.JSONField(
        default=list,
        help_text=_("List of features in the plan, stored as a JSON array."),
    )
    button_text = models.CharField(max_length=50)
    href = models.CharField(max_length=200)
    is_popular = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = _("subscription_plans")
        managed = True
        verbose_name = _("Subscription Plan")
        verbose_name_plural = _("Subscription Plans")


class Vendor(TimeStampedModel):
    user_id = models.UUIDField(
        verbose_name=_("User Id"),
        help_text=_("User ID from Auth Service"),
    )
    name = models.CharField(max_length=255, verbose_name=_("Vendor Name"))
    email = models.EmailField(unique=True, verbose_name=_("Email Address"))
    phone = models.CharField(max_length=20, unique=True, verbose_name=_("Phone Number"))
    address = models.TextField(verbose_name=_("Physical Address"))

    class Meta:
        verbose_name = _("Vendor")
        verbose_name_plural = _("Vendors")
        db_table = "vendors"
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["email"]),
        ]

    def __str__(self):
        return self.name
    
    @property
    def active_plan(self) -> 'VendorPlan':
        return self.plans.first()

    @property
    def plan(self):
        return str(self.active_plan.plan.id) if self.active_plan else None

    @property
    def billing_cycle(self):
        return self.active_plan.billing_cycle if self.active_plan else None



class VendorPlan(TimeStampedModel):
    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.CASCADE,
        related_name="plans",
        verbose_name=_("Vendor"),
    )
    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.CASCADE,
        related_name="vendor_plans",
        verbose_name=_("Subscription Plan"),
    )
    billing_cycle = models.CharField(
        max_length=10,
        choices=BillingCycle.choices,
        default=BillingCycle.MONTHLY,
        verbose_name=_("Billing Cycle"),
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.INACTIVE,
        verbose_name=_("Status"),
    )
    start_date = models.DateTimeField(verbose_name=_("Start Date"), null=True, blank=True)
    end_date = models.DateTimeField(verbose_name=_("End Date"), null=True, blank=True)

    class Meta:
        verbose_name = _("Vendor Plan")
        verbose_name_plural = _("Vendor Plans")
        db_table = "vendor_plans"
        constraints = [
            UniqueConstraint(
                fields=["vendor", "plan"],
                name="unique_vendor_plan"
            ),
        ]
