from django.contrib import admin
from .models import ParkingSlot, Vehicle, ParkingRecord


@admin.register(ParkingSlot)
class ParkingSlotAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'slot_number',
        'is_occupied',
    )

    list_filter = (
        'is_occupied',
    )

    search_fields = (
        'slot_number',
    )


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):

    list_display = (
        'vehicle_number',
        'owner_name',
        'phone_number',
        'vehicle_type',
        'created_at',
    )

    list_filter = (
        'vehicle_type',
    )

    search_fields = (
        'vehicle_number',
        'owner_name',
    )


@admin.register(ParkingRecord)
class ParkingRecordAdmin(admin.ModelAdmin):

    list_display = (
        'vehicle',
        'slot',
        'entry_time',
        'exit_time',
        'parking_fee',
        'is_active',
    )

    list_filter = (
        'is_active',
        'entry_time',
    )

    search_fields = (
        'vehicle__vehicle_number',
    )