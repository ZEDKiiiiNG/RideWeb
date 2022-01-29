from django import forms


class UserForm(forms.Form):
    username = forms.CharField(label="username", max_length=128)
    password = forms.CharField(label="password", max_length=256, widget=forms.PasswordInput)

class RegisterForm(forms.Form):

    username = forms.CharField(label="username", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="password", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="password_confirmed", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="email", widget=forms.EmailInput(attrs={'class': 'form-control'}))


class DriverRigisterForm(forms.Form):

    vehicleType = forms.CharField(max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    licensePlateNumber = forms.CharField(max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    allowedPassengers = forms.IntegerField(widget=forms.NumberInput)
    specialInfo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

class RideForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(label="Time (eg. 14:30)", input_formats=['%H:%M'], widget=forms.TimeInput(format='%H:%M'))
    start = forms.CharField(label="Start Point", max_length=32,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    end = forms.CharField(label="End Point", max_length=32,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    partySize = forms.IntegerField(label="Party Size", widget=forms.TextInput(attrs={'class': 'form-control'}))
    specialText = forms.CharField(label="Special Text", max_length=32,
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))
    isSharable = forms.BooleanField(initial= False, label="Is Sharable?", required=False)
    status = forms.CharField(initial="open", label="Status", max_length=32, disabled=True, widget=forms.TextInput(attrs={'class': 'form-control'}))



