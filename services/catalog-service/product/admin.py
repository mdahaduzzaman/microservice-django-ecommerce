from django.contrib import admin

from product.models import Category, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name",)
    ordering = ("-created_at",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("category", "title", "price", "created_at", "updated_at")
    search_fields = ("name", "category__name")
    ordering = ("-created_at",)
    inlines = [ProductImageInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("category")
