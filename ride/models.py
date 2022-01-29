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




