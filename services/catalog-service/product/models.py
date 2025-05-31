import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_("ID")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class Category(TimeStampedModel):
    name = models.CharField(
        max_length=255, unique=True, verbose_name=_("Category Name")
    )
    slug = models.SlugField(
        max_length=255, unique=True, verbose_name=_("Slug"), blank=True
    )
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subcategories",
        verbose_name=_("Parent Category"),
    )

    class Meta:
        db_table = "categories"
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug or self.name_changed():
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.exclude(pk=self.pk).filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def name_changed(self):
        if not self.pk:
            return True
        try:
            old = Category.objects.get(pk=self.pk)
            return old.name != self.name
        except Category.DoesNotExist:
            return True


class Product(TimeStampedModel):
    category = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.PROTECT,
        verbose_name=_("Category"),
    )
    title = models.CharField(max_length=255, verbose_name=_("Product Title"))
    slug = models.SlugField(
        max_length=255, unique=True, blank=True, verbose_name=_("Slug")
    )
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("Price")
    )
    vendor_id = models.UUIDField(verbose_name=_("Vendor ID"))

    class Meta:
        db_table = "products"
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        indexes = [
            models.Index(fields=["vendor_id"]),
            models.Index(fields=["title"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug or self.name_changed():
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Product.objects.exclude(pk=self.pk).filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def name_changed(self):
        if not self.pk:
            return True
        try:
            old = Product.objects.get(pk=self.pk)
            return old.title != self.title
        except Product.DoesNotExist:
            return True

