from typing import Optional
from rest_framework.viewsets import ModelViewSet
from rest_framework.request import Request
from rest_framework.exceptions import PermissionDenied
from uuid import UUID
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from product.models import Product, Category
from product.serializers import ProductSerializer, CategorySerializer
from product.services import InventoryServiceClient, VendorServiceClient
from product.filters import ProductFilter


@extend_schema(tags=["Category"])
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"


@extend_schema(tags=["Product"])
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related("category")
    serializer_class = ProductSerializer
    lookup_field = "slug"
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_user_id(self, request: Request) -> UUID:
        user_id_str: Optional[str] = request.META.get("HTTP_X_USER_ID")
        if not user_id_str:
            raise PermissionDenied("User ID not provided in header.")
        try:
            return UUID(user_id_str)
        except ValueError:
            raise PermissionDenied("Invalid User ID format.")

    def get_vendor_id(self, request: Request) -> UUID:
        user_id = self.get_user_id(request)
        client = VendorServiceClient()
        vendor_id = client.get_vendor(user_id)
        if not vendor_id:
            raise PermissionDenied("Vendor not found")
        return vendor_id

    def perform_create(self, serializer):
        vendor_id = self.get_vendor_id(self.request)
        serializer.save(vendor_id=vendor_id)

        client = InventoryServiceClient()
        client.create_product_inventory(
            product_id=serializer.instance.id,
            quantity=serializer.validated_data["quantity"],
        )

    def perform_update(self, serializer):
        vendor_id = self.get_vendor_id()
        if not vendor_id:
            raise PermissionDenied("Vendor ID is required.")
        # Optional: Check if product belongs to vendor before update
        if serializer.instance.vendor_id != vendor_id:
            raise PermissionDenied(
                "You cannot update a product that does not belong to you."
            )
        serializer.save(vendor_id=vendor_id)

    def perform_destroy(self, instance):
        vendor_id = self.get_vendor_id()
        if not vendor_id:
            raise PermissionDenied("Vendor ID is required.")
        if instance.vendor_id != vendor_id:
            raise PermissionDenied(
                "You cannot delete a product that does not belong to you."
            )
        instance.delete()


class HealthView(APIView):
    @extend_schema(
        responses={
            "200": {"type": "object", "properties": {"status": {"type": "string"}}}
        },
    )
    def get(self, request) -> Response:
        return Response({"status": "running"})
