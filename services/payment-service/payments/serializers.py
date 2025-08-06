from rest_framework import serializers

from payments.models import PaymentMethod


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = "__all__"


class LineItemSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(
        max_length=500, required=False, allow_blank=True
    )
    amount = serializers.FloatField()
    quantity = serializers.IntegerField(default=1)


class CheckoutSessionSerializer(serializers.Serializer):
    payment_method = serializers.PrimaryKeyRelatedField(
        queryset=PaymentMethod.objects.filter(is_active=True), required=True
    )
    mode = serializers.ChoiceField(choices=["payment", "subscription"], required=True)
    line_items = LineItemSerializer(many=True, required=True)
    currency = serializers.ChoiceField(choices=["usd"], required=True)
    success_url = serializers.URLField(required=True)
    cancel_url = serializers.URLField(required=True)
    metadata = serializers.DictField(required=False, allow_null=True)

class SessionResponseSerializer(serializers.Serializer):
    session_id = serializers.CharField()
    checkout_url = serializers.URLField()
