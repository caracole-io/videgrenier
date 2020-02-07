"""Add Vide Grenier models to admin interface."""
from django.contrib import admin

from .models import Reservation

admin.site.register(Reservation)
