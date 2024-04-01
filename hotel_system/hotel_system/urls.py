"""
URL configuration for hotel_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import include, path

from hotel_system import views

# this file will control which url sends which page

urlpatterns = [
    path("admin/", admin.site.urls),
    path("room/<int:room_id>/", views.room),
    path("hotel_rooms/<int:hotel_id>/", views.hotel_rooms),
    path("", views.index),
    path("employee/", views.employee),
    path("booking/<int:booking_id>", views.booking, name='booking'),
    path("employee/crud/<str:model_name>/", views.crud)
]
