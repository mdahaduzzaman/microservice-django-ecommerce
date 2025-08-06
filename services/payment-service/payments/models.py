import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator


from payments.choices import Status, TransactionType


class TimeStampedModel(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_("ID")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class PaymentMethod(TimeStampedModel):
    """Supported payment methods (Stripe, PayPal, etc.)"""
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    image_url = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "payment_methods"
        managed = True
        verbose_name = "Payment Method"
        verbose_name_plural = "Payment Methods"


class Transaction(TimeStampedModel):
    transaction_id = models.CharField(max_length=200, unique=True)
    user_id = models.UUIDField()
    amount = models.DecimalField(
        max_digits=12, decimal_places=2, validators=[MinValueValidator(0)]
    )
    currency = models.CharField(max_length=3, default="USD")
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    transaction_type = models.CharField(max_length=20, choices=TransactionType.choices)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "transactions"
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        indexes = [
            models.Index(fields=["transaction_id"]),
            models.Index(fields=["user_id", "status"]),
        ]

    def __str__(self):
        return f"{self.transaction_id} - {self.amount} {self.currency}"


class PaymentWebhookLog(TimeStampedModel):
    payload = models.JSONField()
    headers = models.JSONField()
    processed = models.BooleanField(default=False)
    processing_notes = models.TextField(blank=True)

    class Meta:
        db_table = "payment_webhook_logs"
        verbose_name = "Payment Webhook Log"
        verbose_name_plural = "Payment Webhook Logs"
        indexes = [
            models.Index(fields=["processed"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"Webhook Log {self.id} - Processed: {self.processed}"
