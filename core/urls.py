from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    health,
    landing,
    ServiceViewSet,
    ProfessionalViewSet,
    CustomerViewSet,
    OrderViewSet,
    public_order_request,
    join_client_waitlist,
    join_provider_waitlist
)

router = DefaultRouter()
router.register("services", ServiceViewSet, basename="services")
router.register("professionals", ProfessionalViewSet, basename="professionals")
router.register("customers", CustomerViewSet, basename="customers")
router.register("orders", OrderViewSet, basename="orders")

urlpatterns = [
    path("", landing, name="landing"),
    path("health/", health),

    path("api/request-service/", public_order_request, name="public_order_request"),

    path("api/waitlist/client/", join_client_waitlist),
    path("api/waitlist/provider/", join_provider_waitlist),

    path("api/", include(router.urls)),
]
