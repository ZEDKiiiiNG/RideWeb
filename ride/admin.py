from django.contrib import admin

# Register your models here.
from django.contrib import admin
from . import models

admin.site.register(models.User)
admin.site.register(models.Driver)
admin.site.register(models.Ride)
admin.site.register(models.JoinRide)