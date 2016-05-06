from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test import TestCase

from .models import Caracolien


class CaracolienTests(TestCase):
    def setUp(self):
        for guy in 'abc':
            User.objects.create_user(guy, email='%s@example.org' % guy, password=guy)
        a, b, c = Caracolien.objects.order_by('pk')
        a.phone_number = '+33641452777'
        a.adhesion = date.today() - timedelta(days=100)
        b.adhesion = date.today() - timedelta(days=1000)
        a.save()
        b.save()

    # MODELS

    def test_caracolien_str(self):
        a, b, c = Caracolien.objects.order_by('pk')
        self.assertEqual(str(a), 'a')
        self.assertEqual(str(b), 'b')
        self.assertEqual(str(c), 'c')

    def test_adherent(self):
        a, b, c = Caracolien.objects.order_by('pk')
        self.assertTrue(a.adherent())
        self.assertFalse(b.adherent())
        self.assertFalse(c.adherent())
