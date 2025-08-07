from django.contrib import admin

from payments.models import PaymentMethod, SubscriptionPlan


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "image_url")
    search_fields = ("name", "image_url")
    readonly_fields = ("id", "created_at", "updated_at")


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "payment_method",
        "interval",
        "monthly_price",
        "yearly_price",
    )
    search_fields = ("name", "payment_method__name")
    readonly_fields = ("id", "created_at", "updated_at")
