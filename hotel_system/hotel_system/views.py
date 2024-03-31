from django.http import Http404, HttpResponse
from django.shortcuts import render

# this is a python file defining all of the different pages
from hotel_system.models import Amenity, Room, Hotel, HotelChain


# Create your views here.
def index(request):
    all_hotels = Hotel.objects.all()
    hotel_locations = set([hotel.city for hotel in all_hotels])

    filtered_hotels = all_hotels
    if request.GET.getlist("chain"):
        filtered_hotels = all_hotels.filter(hotel_chain_id__in=request.GET.getlist("chain"))
    
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


def employee(request):
    return render(request, "employee.html")
