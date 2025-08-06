from django.contrib import admin

from payments.models import PaymentMethod


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "image_url")
    search_fields = ("name", "image_url")
    readonly_fields = ("id", "created_at", "updated_at")
