from datetime import date, timedelta

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from caracole.models import Caracolien

from .models import Reservation


class VideGrenierTests(TestCase):
    def setUp(self):
        for guy in 'abcd':
            user = User.objects.create_user(guy, email='%s@example.org' % guy, password=guy)
            if guy == 'a':
                caracolien = Caracolien.objects.get(user=user)
                caracolien.adhesion = date.today() - timedelta(days=8)
                caracolien.save()
                Reservation.objects.create(caracolien=caracolien)
            elif guy == 'b':
                Reservation.objects.create(caracolien=user.caracolien)
            elif guy == 'd':
                user.is_staff = True
                user.save()

    # MODELS

    def test_reservation_prix(self):
        for reservation in Reservation.objects.all():
            self.assertEqual(reservation.prix(), 12 if str(reservation) == 'a' else 14)

    # VIEWS

    def test_views_status(self):
        self.client.login(username='c', password='c')
        self.assertEqual(self.client.get(reverse('videgrenier:reservation-create')).status_code, 200)
        self.client.login(username='a', password='a')
        self.assertEqual(self.client.get(reverse('videgrenier:reservation-create')).status_code, 302)
        self.assertEqual(self.client.get(reverse('videgrenier:reservation-detail')).status_code, 200)
        self.assertEqual(self.client.get(reverse('videgrenier:reservation-delete')).status_code, 200)

    def test_reservation_create_view(self):
        self.assertFalse(Reservation.objects.filter(caracolien__user__username='c').exists())
        self.client.login(username='c', password='c')
        self.client.post(reverse('videgrenier:reservation-create'))
        self.assertTrue(Reservation.objects.filter(caracolien__user__username='c').exists())

    def test_reservation_update_view(self):
        reservation = Reservation.objects.get(caracolien__user__username='a')
        self.assertIsNone(reservation.accepte)
        self.client.login(username='d', password='d')
        self.client.get(reverse('videgrenier:reservation-update', kwargs={'pk': reservation.pk, 'accepte': '0'}))
        self.assertFalse(Reservation.objects.get(caracolien__user__username='a').accepte)
        self.client.get(reverse('videgrenier:reservation-update', kwargs={'pk': reservation.pk, 'accepte': '1'}))
        reservation = Reservation.objects.get(caracolien__user__username='a')
        self.assertTrue(Reservation.objects.get(caracolien__user__username='a').accepte)
