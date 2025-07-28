from rest_framework import serializers
from django.db import transaction

from product.models import Product, Category, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image", "is_primary"]

    def validate(self, attrs):
        if (
            attrs.get("is_primary")
            and ProductImage.objects.filter(
                product=attrs["product"], is_primary=True
            ).exists()
        ):
            raise serializers.ValidationError(
                "A product can only have one primary image."
            )
        return attrs


class CategorySerializer(serializers.ModelSerializer):
    subcategories_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description", "parent", "subcategories_count"]

    def get_subcategories_count(self, obj: Category) -> int:
        return obj.subcategories.count()


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = "__all__"

    @transaction.atomic
    def create(self, validated_data: dict) -> Product:
        images_data = validated_data.pop("images", [])
        product = Product.objects.create(**validated_data)
        for image_data in images_data:
            ProductImage.objects.create(product=product, **image_data)
        return product

    @transaction.atomic
    def update(self, instance: Product, validated_data: dict) -> Product:
        images_data = validated_data.pop("images", [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Handle images
        if images_data:
            instance.images.all().delete()
            for image_data in images_data:
                ProductImage.objects.create(product=instance, **image_data)
        return instance
