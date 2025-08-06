from django.contrib import admin

from vendors.models import SubscriptionPlan, Vendor, VendorPlan


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "monthly_price", "yearly_price", "is_popular")
    search_fields = ("name", "description")

    readonly_fields = ("id", "created_at", "updated_at")


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone")
    search_fields = ("name", "email")
    readonly_fields = ("id", "created_at", "updated_at")


@admin.register(VendorPlan)
class VendorPlanAdmin(admin.ModelAdmin):
    list_display = (
        "vendor",
        "plan",
        "billing_cycle",
        "status",
        "start_date",
        "end_date",
    )
    search_fields = ("vendor__name", "plan__name")
    readonly_fields = ("id", "created_at", "updated_at")
