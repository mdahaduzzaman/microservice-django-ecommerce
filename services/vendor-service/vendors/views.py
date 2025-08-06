from typing import Optional
from uuid import UUID
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.request import Request
from drf_spectacular.utils import extend_schema
from rest_framework.generics import RetrieveAPIView
from rest_framework import viewsets

from vendors.models import Vendor, SubscriptionPlan, VendorPlan
from vendors.serializers import (
    CheckoutResponseSerializer,
    CheckoutSessionSerializer,
    VendorCreateSerializer,
    VendorSerializer,
    SubscriptionPlanSerializer,
    VendorPlanSerializer,
)
from vendors.user_service import assign_vendor_role
from vendors.payment_service import PaymentServiceClient


@extend_schema(tags=["Vendor"])
class VendorMeView(APIView):
    serializer_class = VendorSerializer

    def get_user_id(self, request: Request) -> UUID:
        user_id_str: Optional[str] = request.META.get("HTTP_X_USER_ID")
        if not user_id_str:
            raise PermissionDenied("User ID not provided in header.")
        try:
            return UUID(user_id_str)
        except ValueError:
            raise PermissionDenied("Invalid User ID format.")

    def get(self, request: Request) -> Response:
        user_id = self.get_user_id(request)
        vendor = Vendor.objects.filter(user_id=user_id).first()
        if not vendor:
            return Response({"detail": "Vendor not found."}, status=404)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        user_id = self.get_user_id(request)
        if Vendor.objects.filter(user_id=user_id).exists():
            return Response({"detail": "Vendor already exists."}, status=400)

        serializer = VendorCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=user_id)
            # Assign the vendor role to the user
            assign_vendor_role(user_id)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request: Request) -> Response:
        user_id = self.get_user_id(request)
        vendor = Vendor.objects.filter(user_id=user_id).first()
        if not vendor:
            return Response({"detail": "Vendor not found."}, status=404)

        serializer = VendorSerializer(vendor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request: Request) -> Response:
        user_id = self.get_user_id(request)
        vendor = Vendor.objects.filter(user_id=user_id).first()
        if not vendor:
            return Response({"detail": "Vendor not found."}, status=404)
        vendor.delete()
        return Response(status=204)


@extend_schema(tags=["Subscription Plan"])
class SubscriptionPlanView(viewsets.ReadOnlyModelViewSet):
    serializer_class = SubscriptionPlanSerializer
    queryset = SubscriptionPlan.objects.all()


@extend_schema(tags=["Vendor Plan"])
class VendorPlanView(RetrieveAPIView):
    serializer_class = VendorPlanSerializer
    queryset = VendorPlan.objects.all()
    lookup_field = "vendor"


class CreateVendorCheckoutView(APIView):
    @extend_schema(
        request=CheckoutSessionSerializer,
        responses={201: CheckoutResponseSerializer},
    )
    def post(self, request: Request) -> Response:
        serializer = CheckoutSessionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            client = PaymentServiceClient()
            response = client.create_checkout_session(
                **serializer.validated_data,
            )
            return Response(response, status=200)
        except requests.RequestException as e:
            return Response({"detail": str(e)}, status=500)


class HealthView(APIView):
    @extend_schema(
        responses={
            "200": {"type": "object", "properties": {"status": {"type": "string"}}}
        },
    )
    def get(self, request) -> Response:
        return Response({"status": "running"})
