from django.apps import apps
from django.http import Http404, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render

# this is a python file defining all of the different pages
from hotel_system.models import Amenity, Room, Hotel, HotelChain


# Create your views here.
def index(request):
    all_hotels = Hotel.objects.all()
    hotel_locations = set([hotel.address for hotel in all_hotels])

    filtered_hotels = all_hotels
    if request.GET.getlist("chain"):
        filtered_hotels = all_hotels.filter(chain_id__in=request.GET.getlist("chain"))
    
    all_chains = HotelChain.objects.all()
    return render(request, "hotels.html", {"hotels": filtered_hotels, "chains": all_chains,})

def rooms(request, hotel_id):
    return render(request, "rooms.html")


def room(request, room_id):
    try:
        room = Room.objects.get(id=room_id)
    except Room.DoesNotExist:
        raise Http404(f"Room id: {room_id}, does not exist")
    return render(request, "room.html", {"room": room})


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
    return render(request, "crud.html")
