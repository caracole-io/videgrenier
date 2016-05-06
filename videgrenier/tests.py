from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test import TestCase

from caracole.models import Caracolien

from .models import Reservation


class VideGrenierTests(TestCase):
    def setUp(self):
        for guy in 'ab':
            User.objects.create_user(guy, email='%s@example.org' % guy, password=guy)
        caracolien = Caracolien.objects.first()
        caracolien.adhesion = date.today() - timedelta(days=8)
        caracolien.save()
        for caracolien in Caracolien.objects.all():
            Reservation.objects.create(caracolien=caracolien)

    # MODELS

    def test_reservation_prix(self):
        for reservation in Reservation.objects.all():
            self.assertEqual(reservation.prix(), 12 if str(reservation) == 'a' else 14)
