"""Vide Grenier forms."""

from django import forms
from django.contrib.auth.models import User

from .models import Reservation


class ReservationForm(forms.ModelForm):
    """ModelForm for Reservation."""

    class Meta:
        """Meta."""

        model = Reservation
        exclude = ["user", "accepte"]  # noqa: DJ006
        widgets = {
            "birthdate": forms.DateInput(attrs={"type": "date"}),
            "id_date": forms.DateInput(attrs={"type": "date"}),
        }


class UserForm(forms.ModelForm):
    """ModelForm for User."""

    class Meta:
        """Meta."""

        model = User
        fields = ["first_name", "last_name"]
