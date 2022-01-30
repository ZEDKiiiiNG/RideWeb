from django import forms
from datetime import datetime
calendar_widget = forms.widgets.DateInput(attrs={'class': 'date-pick'}, format='%m/%d/%Y')
time_widget = forms.widgets.TimeInput(attrs={'class': 'time-pick'})
valid_time_formats = ['%H:%M', '%I:%M%p', '%I:%M %p']

class UserForm(forms.Form):
    username = forms.CharField(label="username", max_length=128)
    password = forms.CharField(label="password", max_length=256, widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    username = forms.CharField(label="username", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="password", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="password_confirmed", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="email", widget=forms.EmailInput(attrs={'class': 'form-control'}))


class DriverRigisterForm(forms.Form):
    vehicleType = forms.CharField(label="vehicle Type",max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    licensePlateNumber = forms.CharField(label="license Plate Number",max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    allowedPassengers = forms.IntegerField(label="allowed Passengers number",widget=forms.NumberInput)
    specialInfo = forms.CharField(label="special Info",widget=forms.TextInput(attrs={'class': 'form-control'}))

class RideForm(forms.Form):
    end = forms.CharField(label="Destination ",max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    #start to make sure driver know where to pick
    start = forms.CharField(label="Start Area ", max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    arrivalDate = forms.DateField(label="Arrival date",widget=calendar_widget , help_text='ex: 12/23/2018')
    arrivalTime = forms.TimeField(label="Arrival time", widget=time_widget, help_text='ex: 10:30',
                                 input_formats=valid_time_formats)
    partySize = forms.IntegerField( label="Party Passengers number",widget=forms.NumberInput)
    specialRequests = forms.CharField(required=False,label="Special requests",widget=forms.TextInput(attrs={'class': 'form-control'}))
    # vehicleTypeRequest = forms.CharField(label="Vehicle type request",max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    isSharable = forms.BooleanField(required=False,label="Ride sharable",initial= False)
    status = forms.CharField(initial="open", label="Status", max_length=32, disabled=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

class passengerSearchRideForm(forms.Form):
    end = forms.CharField(label="Destination ", max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    earlyArrivalDate = forms.DateField(label="Arrival date", widget=calendar_widget)
    earlyArrivalTime = forms.TimeField(label="Arrival time", widget=time_widget, help_text='ex: 10:30AM',
                                       input_formats=valid_time_formats)
    lateArrivalDate = forms.DateField(label="Arrival date", widget=calendar_widget)
    lateArrivalTime = forms.TimeField(label="Arrival time", widget=time_widget, help_text='ex: 10:30AM',
                                       input_formats=valid_time_formats)
    partySize = forms.IntegerField(label="Party Passengers number", widget=forms.NumberInput)


