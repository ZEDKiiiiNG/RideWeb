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

class Ride(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    driverId = models.IntegerField(default=-1, blank=True)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    start = models.CharField(max_length=32)
    end = models.CharField(max_length=32)
    partySize = models.IntegerField()
    status = models.CharField(max_length=32, default= 'open')
    sharer = models.ManyToManyField(User, related_name= 'sharer')
    isSharable = models.BooleanField(default=False)





