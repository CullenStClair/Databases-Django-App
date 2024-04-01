from django.apps import apps
from django.db import models
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import render

# this is a python file defining all of the different pages
from hotel_system.models import Amenity, Hotel, HotelChain, Room, BookingOrder
from hotel_system.forms import BookingForm


# Create your views here.
def index(request):
    all_hotels = Hotel.objects.all()
    hotel_locations = set([hotel.address for hotel in all_hotels])

    filtered_hotels = all_hotels
    if request.GET.getlist("chain"):
        filtered_hotels = all_hotels.filter(chain_id__in=request.GET.getlist("chain"))

    all_chains = HotelChain.objects.all()
    return render(request, "hotels.html", {"hotels": filtered_hotels, "chains": all_chains, })


def rooms(request, hotel_id):
    return render(request, "rooms.html")


def room(request, room_id):
    try:
        room = Room.objects.get(id=room_id)
    except Room.DoesNotExist:
        raise Http404(f"Room id: {room_id}, does not exist")

    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = BookingForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            check_in_date = form.cleaned_data['check_in_date']
            check_out_date = form.cleaned_data['check_out_date']
            booking_instance = BookingOrder(
                    room=room,
                    customer=form.cleaned_data['customer_id'],
                    check_in_date=check_in_date,
                    check_out_date=check_out_date,
                    cost=room.price * ((check_out_date - check_in_date).days + 1),
                    is_active=True)
            booking_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed')) # send to a booking review page
    # If this is a GET (or any other method) create the default form.
    else:
        form = BookingForm()

    return render(request, "room.html", {"form": form, "room": room})


def hotel(request, hotel_id):
    try:
        hotel = Hotel.objects.get(id=hotel_id)
    except Hotel.DoesNotExist:
        raise Http404(f"Hotel id: {hotel_id}, does not exist")
    return render(request, "rooms.html", {"hotel": hotel})


def employee(request):
    model_names = [model.__name__ for model in apps.get_app_config('hotel_system').get_models()]
    return render(request, "employee.html", {"model_names": model_names})


def crud(request, model_name):
    try:
        Model = apps.get_model("hotel_system", model_name)
    except LookupError:
        raise Http404(f"Table: {model_name}, does not exist in the database")
    rows = Model.objects.all().defer("").values_list()
    fields = [field.name for field in Model._meta.get_fields() if not isinstance(field, models.ManyToOneRel)]
    return render(request, "crud.html", {"model_name": model_name, "rows": rows, "fields": fields})
