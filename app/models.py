from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('dealer', 'Dealer'),
        ('customer', 'Customer'),
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    state = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()

    def __str__(self):
        return self.user.username


class Dealer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name_of_company = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


# -------------------------
# Hotel & HotelRoom Models
# -------------------------

class Hotel(models.Model):
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE, related_name='hotels')
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    amenities = models.JSONField(default=list)
    description = models.TextField(null=True, blank=True)
    floor_count = models.PositiveIntegerField(default=1, help_text="Total number of floors in the hotel")
    Hotel_image=models.ImageField(upload_to='hotel_images/',null=True,blank=True)
    def __str__(self):
        return f"{self.name} - {self.location}"


# class HotelRoom(models.Model):
#     ROOM_TYPE_CHOICES = (
#         ('single', 'Single'),
#         ('double', 'Double'),
#         ('suite', 'Suite'),
#     )

#     hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
#     room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)
#     price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
#     capacity = models.IntegerField()
#     available = models.BooleanField(default=True)

#     def __str__(self):
#         return f"{self.hotel.name} - {self.room_type}"
    
class HotelRoom(models.Model):
    ROOM_TYPE_CHOICES = (
        ('single', 'Single'),
        ('double', 'Double'),
        ('suite', 'Suite'),
    )
    #dealer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    floor_number = models.PositiveIntegerField(default=1)
    room_number = models.CharField(max_length=4)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES, null=True, blank=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    roomImg=models.ImageField(upload_to='room_images/',null=True,blank=True)
    capacity = models.IntegerField(null=True, blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.hotel.name} - Floor {self.floor_number} - Room {self.room_number}"


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    hotel_room = models.ForeignKey(HotelRoom, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    
    num_persons = models.PositiveIntegerField(default=1)
    address_proof = models.FileField(upload_to='address_proofs/')

    def __str__(self):
        return f"Booking for {self.hotel_room} from {self.check_in} to {self.check_out}"


# -------------------------
# Flight Model
# -------------------------

class Flight(models.Model):
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE, related_name='flights')
    airline = models.CharField(max_length=100)
    flight_number = models.CharField(max_length=20, unique=True)
    from_city = models.CharField(max_length=50)
    to_city = models.CharField(max_length=50)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    total_seats = models.IntegerField()
    available_seats = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.flight_number} ({self.from_city} → {self.to_city})"
