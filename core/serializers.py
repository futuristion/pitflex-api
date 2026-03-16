from rest_framework import serializers
from .models import Service, Professional, Customer, Order


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "code", "name", "description", "is_active"]


class ProfessionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professional
        fields = ["id", "name", "phone", "city", "neighborhood", "is_active", "services"]


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "name", "phone"]


class OrderSerializer(serializers.ModelSerializer):
    customer_id = serializers.IntegerField(write_only=True)
    service_id = serializers.IntegerField(write_only=True)
    professional_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "created_at",
            "status",
            "address",
            "reference",
            "neighborhood",
            "scheduled_for",
            "notes",
            "customer",
            "service",
            "professional",
            "customer_id",
            "service_id",
            "professional_id",
        ]
        read_only_fields = ["id", "created_at", "status", "customer", "service", "professional"]

    def create(self, validated_data):
        customer_id = validated_data.pop("customer_id")
        service_id = validated_data.pop("service_id")
        professional_id = validated_data.pop("professional_id", None)

        return Order.objects.create(
            customer_id=customer_id,
            service_id=service_id,
            professional_id=professional_id,
            **validated_data
        )


class OrderStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Order.Status.choices)


class PublicOrderRequestSerializer(serializers.Serializer):
    customer_name = serializers.CharField(max_length=120)
    phone = serializers.CharField(max_length=30)
    service_id = serializers.IntegerField()
    neighborhood = serializers.CharField(max_length=80)

    address = serializers.CharField(required=False, allow_blank=True)
    reference = serializers.CharField(required=False, allow_blank=True)
    notes = serializers.CharField(required=False, allow_blank=True)