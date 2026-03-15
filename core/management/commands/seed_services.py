from django.core.management.base import BaseCommand
from core.models import Service


DEFAULTS = [
    ("tires", "Pneus", "Troca e reparo de pneus"),
    ("battery", "Bateria", "Teste, carga e troca de bateria"),
    ("calibration", "Calibragem", "Ajuste de pressão dos pneus"),
    ("rotation", "Rodízio", "Rodízio de pneus"),
]


class Command(BaseCommand):
    help = "Seed default services"

    def handle(self, *args, **options):
        created = 0

        for code, name, desc in DEFAULTS:
            obj, was_created = Service.objects.get_or_create(
                code=code,
                defaults={
                    "name": name,
                    "description": desc,
                    "is_active": True,
                },
            )
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f"Serviços carregados. Novos: {created}"))
