from django.db import models

# Create your models here.

# set what the primary keys are too
# https://docs.djangoproject.com/en/5.0/topics/db/models/ 

# going to keep all text charfield entries to a max size of 100 for now
# this will prob be better to tweak later on once everything else is solidified

class ChainEmailAddress(models.Model):
    email_address = models.CharField(primary_key=True, max_length=100)
    hotel_chain = models.ForeignKey(HotelChain) # django can use a foreign key object
                                               # i.e. we won't use chain name as the joining

class HotelChain(models.Model):
    name = models.CharField(max_length=100)
    office_address = models.CharField max_length=100)

class ChainPhoneNumber(models.Model):
    phone_number = models.IntegerField(min_value=1000000000, max_value=9999999999)
    hotel_chain = models.ForeignKey(HotelChain) 

class Hotel(models.Model):
    hotel_chain = models.ForeignKey(HotelChain) 
    hotel_id = models.IntegerField()
    hotel_name = models.CharField(max_length=100)
    num_rooms = models.IntegerField(min_value=0)
    star_rating = models.IntegerField(min_value=1, max_value=5)
    email_address = models.CharField(max_length=100)
    managed_by = models.IntegerField() # this should be a foreign key for employee

class HotelPhoneNumbers(models.Model):
    phone_number = models.IntegerField()
    hotel = models.ForeignKey(Hotel)

# import the rest of the schemas here and convert them into django

class Employee(models.Model):
    first_name = models.CharField()
    last_name = models.CharField()
    address = models.CharField()
    ssn = models.IntegerField(min_value=100000000, max_value=999999999)
    position = models.CharField() # write directly in the role of the employee
    works_at = models.ForeignKey(Hotel)
    works_for = models.ForeignKey(Employee)

class Room(models.Model):
    hotel = models.ForeignKey(Hotel)
    room_num = models.IntegerField()
    price = models.FloatField() # maybe tweak this to only contain 2 sig dig if possible
    capcaity = models.IntegerField()
    is_extendable = models.BooleanField()


