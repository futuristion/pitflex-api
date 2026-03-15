from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render

from .models import Service, Professional, Customer, Order
from .serializers import (
    ServiceSerializer,
    ProfessionalSerializer,
    CustomerSerializer,
    OrderSerializer,
    OrderStatusSerializer,
)


def health(request):
    return JsonResponse({"status": "ok", "app": "pitflex"})


def _valid_transition(current: str, new: str) -> bool:
    allowed = {
        Order.Status.REQUESTED: {Order.Status.ACCEPTED, Order.Status.CANCELED},
        Order.Status.ACCEPTED: {Order.Status.ON_THE_WAY, Order.Status.CANCELED},
        Order.Status.ON_THE_WAY: {Order.Status.IN_PROGRESS, Order.Status.CANCELED},
        Order.Status.IN_PROGRESS: {Order.Status.DONE, Order.Status.CANCELED},
        Order.Status.DONE: set(),
        Order.Status.CANCELED: set(),
    }
    return new in allowed.get(current, set())


class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Service.objects.filter(is_active=True).order_by("name")
    serializer_class = ServiceSerializer


class ProfessionalViewSet(viewsets.ModelViewSet):
    queryset = Professional.objects.all().order_by("name")
    serializer_class = ProfessionalSerializer
    filterset_fields = ["city", "neighborhood", "is_active"]


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by("id")
    serializer_class = CustomerSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related("customer", "service", "professional").all().order_by("-id")
    serializer_class = OrderSerializer
    filterset_fields = ["status", "service", "professional", "neighborhood"]

    @action(detail=True, methods=["patch"], url_path="status")
    def set_status(self, request, pk=None):
        order = self.get_object()
        serializer = OrderStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_status = serializer.validated_data["status"]

        if not _valid_transition(order.status, new_status):
            return Response(
                {"detail": f"Transição inválida: {order.status} -> {new_status}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        order.status = new_status
        order.save(update_fields=["status"])
        return Response(OrderSerializer(order).data)

    @action(detail=True, methods=["post"], url_path="accept")
    def accept(self, request, pk=None):
        order = self.get_object()
        professional_id = request.data.get("professional_id")

        if not professional_id:
            return Response({"detail": "professional_id é obrigatório"}, status=400)

        if order.status != Order.Status.REQUESTED:
            return Response({"detail": "Só é possível aceitar pedidos solicitados"}, status=400)

        order.professional_id = int(professional_id)
        order.status = Order.Status.ACCEPTED
        order.save(update_fields=["professional_id", "status"])

        return Response(OrderSerializer(order).data)

def landing(request):
    return render(request, "landing/index.html")