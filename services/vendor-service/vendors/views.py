from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response

from vendors.models import Vendor
from vendors.serializers import VendorSerializer


class VendorViewSet(ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class HealthView(APIView):
    def get(self, request):
        return Response({"status": "running"})
