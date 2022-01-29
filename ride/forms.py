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



