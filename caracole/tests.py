from datetime import date, timedelta

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
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

    # VIEWS

    def test_views_status(self):
        self.assertEqual(self.client.get(reverse('profil')).status_code, 302)
        self.client.login(username='a', password='a')
        self.assertEqual(self.client.get(reverse('profil')).status_code, 200)
        self.assertEqual(self.client.get(reverse('profil-caracolien')).status_code, 200)
        self.assertEqual(self.client.get(reverse('profil-user')).status_code, 200)
        self.assertEqual(self.client.get(reverse('profil-password')).status_code, 200)

    def test_phone(self):
        self.client.login(username='b', password='b')
        self.client.post(reverse('profil-caracolien'), {'phone_number': '06 424.83 000', 'address': ''})
        self.assertEqual(Caracolien.objects.get(user__username='b').phone_number, '+33642483000')
