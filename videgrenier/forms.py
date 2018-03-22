from django import forms
from django.contrib.auth.models import User

from .models import Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        exclude = ['user', 'accepte']
        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
            'id_date': forms.DateInput(attrs={'type': 'date'}),
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
