from django.db import models

# Create your models here.

# set what the primary keys are too
# https://docs.djangoproject.com/en/5.0/topics/db/models/ 

# going to keep all text charfield entries to a max size of 100 for now
# this will prob be better to tweak later on once everything else is solidified

# need to add primary keys, and figure out composite PKs
# need to add not nulls?

class ChainEmailAddress(models.Model):
    email_address = models.CharField(primary_key=True, max_length=100)
    hotel_chain = models.ForeignKey(HotelChain, on_delete = models.CASCADE) # django can use a foreign key object
                                               # i.e. we won't use chain name as the joining

class HotelChain(models.Model):
    name = models.CharField(max_length=100)
    office_address = models.CharField(max_length=100)

class ChainPhoneNumber(models.Model):
    phone_number = models.IntegerField(min_value=1000000000, max_value=9999999999)
    hotel_chain = models.ForeignKey(HotelChain, on_delete = models.CASCADE) 

class Hotel(models.Model):
    hotel_chain = models.ForeignKey(HotelChain, on_delete = models.CASCADE) 
    hotel_id = models.IntegerField() # autoincrement
    hotel_name = models.CharField(max_length=100)
    num_rooms = models.IntegerField(min_value=0)
    star_rating = models.IntegerField(min_value=1, max_value=5)
    email_address = models.CharField(max_length=100)
    managed_by = models.ForeignKey(Employee, on_delete = models.CASCADE)

class HotelPhoneNumbers(models.Model):
    phone_number = models.IntegerField()
    hotel = models.ForeignKey(Hotel, on_delete = models.CASCADE)

class Employee(models.Model):
    employee_id = models.IntegerField()
    first_name = models.CharField()
    last_name = models.CharField()
    address = models.CharField()
    ssn = models.IntegerField(min_value=100000000, max_value=999999999)
    position = models.CharField() # write directly in the role of the employee
    works_at = models.ForeignKey(Hotel)
    works_for = models.ForeignKey(Employee)

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete = models.CASCADE)
    room_num = models.IntegerField()
    price = models.FloatField() # maybe tweak this to only contain 2 sig dig if possible
    capcaity = models.IntegerField()
    is_extendable = models.BooleanField()
    # composite primary key (hotel_id, room_num)

class Amenity(models.Model):
    hotel_id = models.ForeignKey(Room, on_delete = models.CASCADE) # this should technically be a composite foreign key
    room_num = models.ForeignKey(Room, on_delete = models.CASCADE)
    amenity_type = models.CharField(max_length=100)
    # composite primary key (hotel_id, room_num)

class Issue(models.Model):
    issue_id = models.IntegerField() # autoincrement
    hotel_id = models.ForeignKey(Room, on_delete = models.CASCADE)
    room_num = models.ForeignKey(Room, on_delete = models.CASCADE)
    date_reported = models.CharField(max_length=100)
    issue_type = models.CharField(max_length=100)
    # composite primary key (hotel_id, room_num)

class BookingOrder(models.Model):
    hotel_id = models.ForeignKey(Room, on_delete = models.CASCADE)
    room_num = models.ForeignKey(Room, on_delete = models.CASCADE)
    booking_id = models.IntegerField() # autoincrement
    customer_id = models.ForeignKey(Customer, on_delete = models.CASCADE)
    booking_date = models.CharField(max_length = 100) # change dates to ISO timestamp?
    check_in_date = models.CharField(max_length = 100) 
    check_out_date = models.CharField(max_length = 100) 
    cost = models.FloatField() # maybe tweak this to only contain 2 sig dig if possible
    is_active = models.BooleanField()

class Customer(models.Model):
    customer_id = models.IntegerField() # PK, autoincrement
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField()
    identification_type = models.CharField()
    identification_value = models.CharField()
    registration_date = models.CharField() # change dates to ISO timestamp?

class BookingArchive(models.Model):
    hotel_id = models.IntegerField()
    room_num = models.IntegerField()
    booking_id = models.IntegerField()
    customer_id = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    booking_date = models.CharField(max_length = 100) # change dates to ISO timestamp?
    check_in_date = models.CharField(max_length = 100) 
    check_out_date = models.CharField(max_length = 100) 

class RentingArchive(models.Model):
    hotel_id = models.IntegerField()
    room_num = models.IntegerField()
    booking_id = models.IntegerField()
    customer_id = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    booking_date = models.CharField(max_length = 100) # change dates to ISO timestamp?
    check_in_date = models.CharField(max_length = 100) 
    check_out_date = models.CharField(max_length = 100) 

