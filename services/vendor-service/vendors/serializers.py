from rest_framework import serializers

from vendors.models import Vendor


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        exclude = ["created_at", "updated_at"]
