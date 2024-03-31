from django.http import Http404, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render

# this is a python file defining all of the different pages
from hotel_system.models import Amenity, Hotel, Room


# Create your views here.
def index(request):
    hotels = Hotel.objects.all()
    return render(request, "hotels.html", {"hotels": hotels})


def rooms(request, hotel_id):
    return render(request, "rooms.html")


def room(request, room_id):
    try:
        room = Room.objects.get(id=room_id)
    except Room.DoesNotExist:
        raise Http404(f"Room id: {room_id}, does not exist")
    return render(request, "room.html", {"room": room})


def employee(request):
    if request.method == "GET":
        return render(request, "employee.html")
    elif request.method == "POST":
        raise HttpResponseNotAllowed("Not implemented")
        # return render(request, "employee.html")
