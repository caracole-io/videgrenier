from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test import TestCase

from caracole.models import Caracolien

from .models import Reservation


class VideGrenierTests(TestCase):
    def setUp(self):
        users = (User.objects.create_user(guy, email='%s@example.org' % guy, password=guy) for guy in 'ab')
        caracoliens = [Caracolien(user=user) for user in users]
        caracoliens[0].adhesion = date.today() - timedelta(days=8)
        for caracolien in caracoliens:
            caracolien.save()
            Reservation(caracolien=caracolien).save()

    # MODELS

    def test_reservation_str(self):
        self.assertEqual(str(Reservation.objects.first()), 'a')

    def test_reservation_prix(self):
        a, b = Reservation.objects.all()
        self.assertEqual(a.prix(), 12)
        self.assertEqual(b.prix(), 14)
