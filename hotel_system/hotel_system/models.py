from django.db import models

# Create your models here.
class Room(models.Model):
    hotel_id = models.IntegerField()
    chain_name = models.CharField(max_length=100)
    hotel_name = models.CharField(max_length=100)
    num_rooms = models.IntegerField()
    star_rating = models.IntegerField()
    email_address = models.CharField(max_length=100)
    managed_by = models.IntegerField()

# import the rest of the schemas here and convert them into django
