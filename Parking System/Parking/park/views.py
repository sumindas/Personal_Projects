from django.shortcuts import render
from django.contrib import messages
from django.db import transaction

from .models import Vehicle, ParkingSlot, ParkingRecord

def dashboard(request):

    # =====================================================
    # HANDLE FORM SUBMISSION
    # =====================================================

    if request.method == "POST":

        action = request.POST.get("action")

        # =================================================
        # ADD / PARK VEHICLE
        # =================================================

        if action == "park":

            vehicle_number = request.POST.get(
                "vehicle_number",
                ""
            ).strip().upper()

            owner_name = request.POST.get(
                "owner_name",
                ""
            ).strip()

            phone = request.POST.get(
                "phone",
                ""
            ).strip()

            vehicle_type = request.POST.get(
                "vehicle_type",
                ""
            ).strip()


            # -----------------------------
            # VALIDATION
            # -----------------------------

            if not vehicle_number:
                messages.error(
                    request,
                    "Vehicle number is required."
                )

                return redirect_dashboard(request)


            if not owner_name:
                messages.error(
                    request,
                    "Owner name is required."
                )

                return redirect_dashboard(request)


            if not phone:
                messages.error(
                    request,
                    "Phone number is required."
                )

                return redirect_dashboard(request)


            if not vehicle_type:

                messages.error(
                    request,
                    "Please select a vehicle type."
                )

                return redirect_dashboard(request)


            # =================================================
            # CHECK DUPLICATE ACTIVE VEHICLE
            # =================================================

            existing_record = ParkingRecord.objects.filter(
                vehicle__vehicle_number=vehicle_number,
                is_active=True
            ).first()


            if existing_record:

                messages.error(
                    request,
                    f"Vehicle {vehicle_number} is already parked "
                    f"in P{existing_record.slot.slot_number}."
                )

                return redirect_dashboard(request)


            # =================================================
            # FIND AVAILABLE SLOT
            # =================================================

            slot = ParkingSlot.objects.filter(
                is_occupied=False
            ).order_by(
                "slot_number"
            ).first()


            if not slot:

                messages.error(
                    request,
                    "Parking is full. No slots are available."
                )

                return redirect_dashboard(request)


            # =================================================
            # CREATE / UPDATE VEHICLE
            # =================================================

            vehicle, created = Vehicle.objects.get_or_create(
                vehicle_number=vehicle_number,
                defaults={
                    "owner_name": owner_name,
                    "phone": phone,
                    "vehicle_type": vehicle_type,
                }
            )


            if not created:

                vehicle.owner_name = owner_name
                vehicle.phone = phone
                vehicle.vehicle_type = vehicle_type
                vehicle.save()


            # =================================================
            # CREATE PARKING RECORD
            # =================================================

            with transaction.atomic():

                ParkingRecord.objects.create(
                    vehicle=vehicle,
                    slot=slot,
                    is_active=True
                )

                slot.is_occupied = True
                slot.save()


            messages.success(
                request,
                f"Vehicle {vehicle_number} parked successfully "
                f"in P{slot.slot_number}."
            )

            return redirect_dashboard(request)


        # =================================================
        # REMOVE VEHICLE
        # =================================================

        elif action == "remove":

            vehicle_number = request.POST.get(
                "vehicle_number",
                ""
            ).strip().upper()


            if not vehicle_number:

                messages.error(
                    request,
                    "Please enter the vehicle number."
                )

                return redirect_dashboard(request)


            record = ParkingRecord.objects.filter(
                vehicle__vehicle_number=vehicle_number,
                is_active=True
            ).select_related(
                "vehicle",
                "slot"
            ).first()


            # -----------------------------
            # VEHICLE NOT FOUND
            # -----------------------------

            if not record:

                messages.error(
                    request,
                    f"No active parking record found for "
                    f"{vehicle_number}."
                )

                return redirect_dashboard(request)


            slot_number = record.slot.slot_number


            # =================================================
            # REMOVE PARKING RECORD
            # =================================================

            with transaction.atomic():

                record.is_active = False
                record.save()

                record.slot.is_occupied = False
                record.slot.save()


            messages.success(
                request,
                f"Vehicle {vehicle_number} removed successfully "
                f"from P{slot_number}."
            )

            return redirect_dashboard(request)


    # =====================================================
    # PARKING SLOTS
    # =====================================================

    slots = ParkingSlot.objects.all().order_by(
        "slot_number"
    )


    # Attach active parking record to each slot
    for slot in slots:

        slot.active_record = ParkingRecord.objects.filter(
            slot=slot,
            is_active=True
        ).select_related(
            "vehicle"
        ).first()


    # =====================================================
    # SUMMARY
    # =====================================================

    total_slots = slots.count()

    occupied_slots = slots.filter(
        is_occupied=True
    ).count()

    available_slots = slots.filter(
        is_occupied=False
    ).count()


    # =====================================================
    # ACTIVE VEHICLES
    # =====================================================

    active_records = ParkingRecord.objects.filter(
        is_active=True
    ).select_related(
        "vehicle",
        "slot"
    ).order_by(
        "-entry_time"
    )


    context = {

        "slots": slots,

        "total_slots": total_slots,

        "occupied_slots": occupied_slots,

        "available_slots": available_slots,

        "active_records": active_records,

    }


    return render(
        request,
        "parking/dashboard.html",
        context
    )


def redirect_dashboard(request):

    from django.shortcuts import redirect

    return redirect("dashboard")