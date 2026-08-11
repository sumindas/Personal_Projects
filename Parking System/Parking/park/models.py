from email.policy import default
from django.db import models

# Create your models here.
class ParkingSlot(models.Model):

    slot_number = models.PositiveIntegerField(
        unique=True
    )

    is_occupied = models.BooleanField(
        default=False
    )
    
    def __str__(self):
        return f"Slot {self.slot_number}"


class Vehicle(models.Model):

    VEHICLE_TYPES = (
        ('BIKE', 'bike'),
        ('CAR', 'car'),
        ('AUTO', 'auto'),
    )
    
    vehicle_type = models.CharField(
        max_length=20,
        choices=VEHICLE_TYPES
    )

    vehicle_number = models.CharField(
        max_length=20,
        unique=True
    )

    owner_name = models.CharField(
        max_length=100
    )

    phone_number = models.CharField(
        max_length=20
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.vehicle_number} - {self.owner_name}"



class ParkingRecord(models.Model):

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE
    )

    slot = models.ForeignKey(
        ParkingSlot,
        on_delete=models.CASCADE
    )

    entry_time = models.DateTimeField(
        auto_now_add=True
    )

    exit_time = models.DateTimeField(
        null=True,
        blank=True
    )

    parking_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default = 0
    )

    is_active = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.vehicle.vehicle_number} - {self.slot.slot_number}"
    