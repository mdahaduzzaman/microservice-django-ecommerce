from typing import Optional
from uuid import UUID
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.request import Request
from drf_spectacular.utils import extend_schema

from vendors.models import Vendor
from vendors.serializers import VendorSerializer
from vendors.user_service import assign_vendor_role


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

        serializer = VendorSerializer(data=request.data)
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


class HealthView(APIView):
    @extend_schema(
        responses={
            "200": {"type": "object", "properties": {"status": {"type": "string"}}}
        },
    )
    def get(self, request) -> Response:
        return Response({"status": "running"})
