from django.utils import timezone
from django.http import Http404
from django.shortcuts import redirect, render
from django.db.models import Count
from .models import Table
from .forms import TableForm
from .tables_details import TABLES, DURATION, OPENING, CLOSING, LAST_SEATING


def home(request):
    return render(request, "index.html")


def booking(request):
    form = TableForm()

    if request.method == "POST":
        form = TableForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("booking_list")
        else:
            form = form

    return render(request, "booking.html", {"form": form})


def booking_list(request):
    message = None

    today = timezone.now().date()

    week_offset = int(request.GET.get("week_offset", 0))

    start_of_week = (
        today
        - timezone.timedelta(days=today.weekday())
        + timezone.timedelta(weeks=week_offset)
    )
    end_of_week = start_of_week + timezone.timedelta(days=6)

    bookings = Table.objects.filter(date__range=[start_of_week, end_of_week])

    if not bookings.exists():
        message = "No bookings found for this week."

    weekdays = [
        (start_of_week + timezone.timedelta(days=i)).strftime("%A") for i in range(7)
    ]

    available_tables = len(TABLES)
    remaining_capacity_data = []

    for day_index in range(7):
        date = start_of_week + timezone.timedelta(days=day_index)

        # Calculate available capacity for the day
        total_minutes = CLOSING - OPENING
        booking_slots = total_minutes // DURATION
        available_capacity = available_tables * booking_slots

        # Calculate booked capacity for the day
        bookings = Table.objects.filter(date=date)
        booked_capacity = bookings.count() or 0

        # Calculate remaining capacity for the day
        remaining_capacity = max(0, available_capacity - booked_capacity)

        # Calculate remaining capacity percentage for the day
        remaining_capacity_percentage = (
            100 * remaining_capacity / available_capacity
            if available_capacity > 0
            else 0
        )

        remaining_capacity_data.append(
            {
                "day": weekdays[day_index],
                "remaining_capacity": remaining_capacity,
                "remaining_capacity_percentage": remaining_capacity_percentage,
            }
        )

    context = {
        "weekdays": weekdays,
        "bookings": bookings,
        "remaining_capacity_data": remaining_capacity_data,
        "week_offset": week_offset,
        "message": message,
    }

    return render(request, "booking_list.html", context)


def booking_detail(request, pk):
    try:
        booking = Table.objects.get(pk=pk)
    except Table.DoesNotExist:
        raise Http404("Booking does not exist.")

    return render(request, "booking_details.html", {"booking": booking})


def booking_edit(request, pk):
    try:
        booking = Table.objects.get(pk=pk)
    except Table.DoesNotExist:
        raise Http404("Booking does not exist.")

    form = TableForm(instance=booking)

    if request.method == "POST":
        form = TableForm(request.POST, instance=booking)

        if form.is_valid():
            form.save()
            return redirect("booking_list")
        else:
            form = form

    return render(request, "booking.html", {"form": form})


def booking_delete(request, pk):
    try:
        booking = Table.objects.get(pk=pk)
    except Table.DoesNotExist:
        raise Http404("Booking does not exist.")

    booking.delete()

    return redirect("booking_list")
