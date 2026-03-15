from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import health, ServiceViewSet, ProfessionalViewSet, CustomerViewSet, OrderViewSet
from .views import landing

router = DefaultRouter()
router.register("services", ServiceViewSet, basename="services")
router.register("professionals", ProfessionalViewSet, basename="professionals")
router.register("customers", CustomerViewSet, basename="customers")
router.register("orders", OrderViewSet, basename="orders")

urlpatterns = [
    path("", landing, name="landing"),
    path("health/", health),
    path("api/", include(router.urls)),    
]
