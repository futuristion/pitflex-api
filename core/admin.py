from django.contrib import admin
from .models import Service, Professional, Customer, Order


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "code")


@admin.register(Professional)
class ProfessionalAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "neighborhood", "is_active")
    list_filter = ("is_active", "city")
    search_fields = ("name", "phone", "neighborhood")
    filter_horizontal = ("services",)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "phone")
    search_fields = ("name", "phone")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "service", "customer", "professional", "status", "neighborhood")
    list_filter = ("status", "service", "created_at")
    search_fields = ("customer__name", "professional__name", "address")
