from django.shortcuts import render
from django.http import HttpResponse

# this is a python file defining all of the different pages
from .models import Room, Amenity

# Create your views here.
def index(request):
   return render(request, "rooms.html")
   #return HttpResponse("Hello world!")

def rooms(request):
    return render(request, "rooms.html")

def hotels(request):
    return render(request, "hotels.html")

# page for a specific room
def room(request, room_id):
    try:
        room_info = Room.objects.get(pk=room_id)
    except Room.DoesNotExist:
        raise Http404(f"Room id: {room_id}, does not exist")
    return render(request, "room.html", {"room_info": room_info}) 


    
