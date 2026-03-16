from django.db import models


class Service(models.Model):
    code = models.SlugField(unique=True)
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=220, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Professional(models.Model):
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=80, default="Fortaleza")
    neighborhood = models.CharField(max_length=80, blank=True)
    is_active = models.BooleanField(default=True)
    services = models.ManyToManyField(Service, blank=True)

    def __str__(self):
        return f"{self.name} ({self.city})"


class Customer(models.Model):
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    class Status(models.TextChoices):
        REQUESTED = "requested", "Solicitado"
        ACCEPTED = "accepted", "Aceito"
        ON_THE_WAY = "on_the_way", "A caminho"
        IN_PROGRESS = "in_progress", "Em execução"
        DONE = "done", "Finalizado"
        CANCELED = "canceled", "Cancelado"

    created_at = models.DateTimeField(auto_now_add=True)

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="orders")
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name="orders")
    professional = models.ForeignKey(
        Professional,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="orders"
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.REQUESTED
    )

    address = models.CharField(max_length=200)
    reference = models.CharField(max_length=120, blank=True)
    neighborhood = models.CharField(max_length=80, blank=True)
    scheduled_for = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"#{self.id} {self.service.name} - {self.status}"


class ClientWaitlist(models.Model):
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    neighborhood = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProviderWaitlist(models.Model):
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    service_type = models.CharField(max_length=120)
    neighborhood = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name