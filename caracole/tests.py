from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test import TestCase

from .models import Caracolien


class CaracolienTests(TestCase):
    def setUp(self):
        a, b, c = (User.objects.create_user(guy, email='%s@example.org' % guy, password=guy) for guy in 'abc')
        Caracolien(user=a, phone_number='+33641452777', adhesion=date.today() - timedelta(days=100)).save()
        Caracolien(user=b, adhesion=date.today() - timedelta(days=1000)).save()
        Caracolien(user=c).save()

    # MODELS

    def test_caracolien_str(self):
        a, b, c = Caracolien.objects.all()
        self.assertEqual(str(a), 'a')
        self.assertEqual(str(b), 'b')
        self.assertEqual(str(c), 'c')

    def test_adherent(self):
        a, b, c = Caracolien.objects.all()
        self.assertTrue(a.adherent())
        self.assertFalse(b.adherent())
        self.assertFalse(c.adherent())
