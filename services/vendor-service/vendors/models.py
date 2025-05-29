import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_("ID")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        abstract = True
        ordering = ["-created_at"]


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
