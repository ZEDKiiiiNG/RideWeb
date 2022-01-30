from django.utils import timezone
from datetime import datetime
from django.db import models

# Create your models here.
from django.db import models


class User(models.Model):
    '''base user class can be driver'''


    name = models.CharField(max_length=128,unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    isDriver = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Driver(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicleType = models.CharField(max_length=32)
    licensePlateNumber = models.CharField(max_length=32)
    allowedPassengers = models.IntegerField()
    specialInfo = models.TextField(blank=True, default="")

    def __str__(self):
        return self.licensePlateNumber

class JoinRide(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    partySize = models.IntegerField()
    def __str__(self):
        return str(self.partySize)

class Ride(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, null= True, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    start = models.CharField(max_length=32)
    end = models.CharField(max_length=32)
    partySize = models.IntegerField(default=0)
    # open, confirmed or complete
    status = models.CharField(max_length=32, default= 'open')
    # sharer = models.ManyToManyField(User, related_name= 'sharer')
    # sharer = models.ForeignKey(JoinRide, null= True, on_delete=models.CASCADE)
    sharer = models.ManyToManyField(JoinRide, blank=True, related_name='sharer')
    isSharable = models.BooleanField(default=False)
    specialRequests = models.TextField(blank=True, default="")

    def __str__(self):
        return self.start + self.end






