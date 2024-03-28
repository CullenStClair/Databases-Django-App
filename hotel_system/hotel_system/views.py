from django.shortcuts import render
from django.http import HttpResponse

# this is a python file defining all of the different pages

# Create your views here.
def index(request):
    return HttpResponse("Hello world!")

def rooms(request):
    return HttpResponse("This is the rooms page")
