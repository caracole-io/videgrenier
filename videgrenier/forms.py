from django.contrib.auth.models import User  # TODO settings.AUTH_USER_MODEL
from django.forms import ModelForm

from .models import Reservation


class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        exclude = ['user', 'accepte']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
