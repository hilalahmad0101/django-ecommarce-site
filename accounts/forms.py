from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Address

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address', 'city', 'postal_code', 'country', 'profile_image']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address_type', 'address', 'city', 'postal_code', 'country']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }
