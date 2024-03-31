from django.db import models

# Create your models here.

# https://docs.djangoproject.com/en/5.0/topics/db/models/

# going to keep all text charfield entries to a max size of 100 for now
# this will prob be better to tweak later on once everything else is solidified

# used https://stackoverflow.com/a/55786819 for creating composite primary keys
# AutoField used for autoincrementing IntegerField
# DateTimeField used for timestamps


class HotelChain(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    office_address = models.CharField(max_length=100)


class Hotel(models.Model):
    hotel_chain = models.ForeignKey('HotelChain', on_delete=models.CASCADE, related_name='hotels')
    hotel_id = models.AutoField(primary_key=True)
    hotel_name = models.CharField(max_length=100)
    num_rooms = models.PositiveIntegerField()
    star_rating = models.IntegerField()
    email_address = models.CharField(max_length=100)
    managed_by = models.ForeignKey('Employee', on_delete=models.CASCADE)
    city = models.CharField(max_length=100)

    @property
    def max_price(self):
        rooms = self.rooms.all()
        return round(rooms.aggregate(models.Max("price"))['price__max'], 2)

    @property
    def min_price(self):
        rooms = self.rooms.all()
        return round(rooms.aggregate(models.Min("price"))['price__min'], 2)


    class Meta:  # this enforces star rating constraints on a database level (it seems this is the only way to do this)
        constraints = [models.CheckConstraint(check=models.Q(star_rating__gte=1) & models.Q(star_rating__lte=5),
                                              name="star rating must be between 1 and 5")]


class ChainEmailAddress(models.Model):
    email_address = models.CharField(max_length=100, primary_key=True)
    hotel_chain = models.ForeignKey('HotelChain', on_delete=models.CASCADE)  # django can use a foreign key object
    # i.e. we won't use chain name as the joining


class ChainPhoneNumber(models.Model):
    phone_number = models.IntegerField(primary_key=True)
    hotel_chain = models.ForeignKey('HotelChain', on_delete=models.CASCADE)

    class Meta:  # phone number validation, should look into doing with a phone number field
        constraints = [models.CheckConstraint(check=models.Q(phone_number__gte=1000000000) & models.Q(phone_number__lt=9999999999),
                                              name="must enter valid phone number")]


class HotelPhoneNumbers(models.Model):
    phone_number = models.IntegerField(primary_key=True)
    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE) # this doesn't seem quite right
                                                               # shouldn't really need a FK

class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    ssn = models.IntegerField()
    position = models.CharField(max_length=100)  # write directly in the role of the employee
    works_at = models.ForeignKey('Hotel', null=True, on_delete=models.SET_NULL, related_name='employees')
    works_for = models.ForeignKey('Employee', null=True, on_delete=models.SET_NULL, related_name='employing')

    class Meta:  # ssn validation
        constraints = [models.CheckConstraint(check=models.Q(ssn__gte=100000000) & models.Q(ssn__lt=999999999),
                                              name="must enter valid ssn")]

class Room(models.Model):
    hotel_id = models.ForeignKey('Hotel', on_delete=models.CASCADE, related_name='rooms')
    room_num = models.IntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    capacity = models.IntegerField()
    is_extendable = models.BooleanField()

    class Meta:  # composite primary key (hotel_id, room_num)
        constraints = [models.UniqueConstraint(fields=['hotel_id', 'room_num'], name='Room primary key')]


class Amenity(models.Model):
    room_id = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='amenities')
#    hotel_id = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='Amenity_hotel_id')
#    room_num = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='Amenity_room_num')
    amenity_type = models.CharField(max_length=100)
#    class Meta: # composite primary key (hotel_id, room_num)
#        constraints = [models.UniqueConstraint(fields=['hotel_id', 'room_num'], name='Amenity primary key')]

    class Meta:  # composite primary key (hotel_id, room_num)
        constraints = [models.UniqueConstraint(fields=['room_id', 'amenity_type'], name='Amenity primary key')]


class Issue(models.Model):
    room_id = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='issues')
    issue_id = models.AutoField(primary_key=True)
    # hotel_id = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='Issue_hotel_id')
    # room_num = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='Issue_room_num')
    date_reported = models.CharField(max_length=100)
    issue_type = models.CharField(max_length=100)


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    identification_type = models.CharField(max_length=100)
    identification_value = models.CharField(max_length=100)
    registration_date = models.DateTimeField(auto_now_add=True)


class BookingOrder(models.Model):
    room_id = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='orders')
    # hotel_id = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="BookingOrder_hotel_id")
    # room_num = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="BookingOrder_room_num")
    booking_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey('Customer', on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    check_in_date = models.DateTimeField()
    check_out_date = models.DateTimeField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField()


class BookingArchive(models.Model):
    hotel_id = models.IntegerField()
    room_num = models.IntegerField()
    booking_id = models.IntegerField(primary_key=True)
    customer_id = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    booking_date = models.DateTimeField(auto_now_add=True)
    check_in_date = models.CharField(max_length=100)
    check_out_date = models.CharField(max_length=100)


class RentingArchive(models.Model):
    hotel_id = models.IntegerField()
    room_num = models.IntegerField()
    booking_id = models.IntegerField(primary_key=True)
    customer_id = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    booking_date = models.DateTimeField(auto_now_add=True)
    check_in_date = models.CharField(max_length=100)
    check_out_date = models.CharField(max_length=100)
