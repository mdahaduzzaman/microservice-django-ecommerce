from rest_framework import serializers
from django.db import transaction

from vendors.models import Vendor, SubscriptionPlan, VendorPlan
from vendors.choices import BillingCycle


class VendorSerializer(serializers.ModelSerializer):
    plan = serializers.ReadOnlyField()
    billing_cycle = serializers.ReadOnlyField()
    class Meta:
        model = Vendor
        exclude = ["created_at", "updated_at", "user_id"]


class VendorCreateSerializer(serializers.ModelSerializer):
    plan = serializers.PrimaryKeyRelatedField(queryset=SubscriptionPlan.objects.all())
    billing_cycle = serializers.ChoiceField(choices=BillingCycle.choices)

    class Meta:
        model = Vendor
        fields = ["name", "email", "phone", "address", "plan", "billing_cycle"]

    @transaction.atomic
    def create(self, validated_data):
        plan = validated_data.pop("plan")
        billing_cycle = validated_data.pop("billing_cycle")
        vendor = Vendor.objects.create(**validated_data)

        VendorPlan.objects.create(
            vendor=vendor,
            plan=plan,
            billing_cycle=billing_cycle,
        )
        return vendor
    
    @transaction.atomic
    def update(self, instance, validated_data):
        plan = validated_data.pop("plan", None)
        billing_cycle = validated_data.pop("billing_cycle", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if plan:
            VendorPlan.objects.update_or_create(
                vendor=instance,
                defaults={"plan": plan, "billing_cycle": billing_cycle}
            )

        return instance


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        exclude = ["created_at", "updated_at"]


class VendorPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorPlan
        exclude = ["created_at", "updated_at"]
