from django.core.management.base import BaseCommand
from park.models import ParkingSlot


class Command(BaseCommand):

    help = "Create 100 parking slots"

    def handle(self, *args, **kwargs):

        for number in range(1, 101):

            ParkingSlot.objects.get_or_create(
                slot_number=number
            )

        self.stdout.write(
            self.style.SUCCESS(
                "100 parking slots created successfully."
            )
        )