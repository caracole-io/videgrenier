from datetime import date, timedelta
from random import randint

from django.contrib.auth.models import User
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase

from .models import Reservation


def infos(guy):
    birthdate = date(1970, 1, 1) + timedelta(days=randint(1, 1E4))
    age = (date.today() - birthdate).days
    return {
        'birthdate': birthdate,
        'birthplace': 'birthplace of %s' % guy,
        'id_num': 'id number of %s' % guy,
        'id_date': date.today() - timedelta(days=randint(1, age)),
        'id_org': 'id issuer of %s' % guy,
        'plaque': 'plaque of %s' % guy,
    }


class VideGrenierTests(TestCase):
    def setUp(self):
        for guy in 'abcd':
            user = User.objects.create_user(guy, email='%s@example.org' % guy, password=guy)
            if guy == 'a':
                Reservation.objects.create(caracolien=user.caracolien, **infos(guy))
                user.caracolien.adhesion = date.today() - timedelta(days=8)
                user.caracolien.save()
            elif guy == 'b':
                Reservation.objects.create(caracolien=user.caracolien, **infos(guy))
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
        self.assertEqual(self.client.get(reverse('videgrenier:reservation-update')).status_code, 200)
        self.assertEqual(self.client.get(reverse('videgrenier:reservation-delete')).status_code, 200)

    def test_reservation_create_view(self):
        self.assertFalse(Reservation.objects.filter(caracolien__user__username='c').exists())
        self.client.login(username='c', password='c')
        self.client.post(reverse('videgrenier:reservation-create'), infos('c'))
        self.assertTrue(Reservation.objects.filter(caracolien__user__username='c').exists())

    def test_reservation_update_view(self):
        reservation = Reservation.objects.get(caracolien__user__username='a')
        self.assertIsNone(reservation.accepte)
        self.client.login(username='d', password='d')  # d est staff

        # d refuse la réservation: la réservation est refusée, a & c reçoivent des mails correspondants
        self.client.get(reverse('videgrenier:reservation-moderate', kwargs={'pk': reservation.pk, 'accepte': '0'}))
        self.assertFalse(Reservation.objects.get(caracolien__user__username='a').accepte)
        email_manager = mail.outbox[-1]
        email_user = mail.outbox[-2]
        self.assertEqual(email_user.to, ['a@example.org'])
        self.assertIn('grenier est désormais refusée', email_user.body)
        self.assertIn('de a est désormais refusée', email_manager.body)

        # d accept la réservation: la réservation est acceptée, a & c reçoivent des mails correspondants
        self.client.get(reverse('videgrenier:reservation-moderate', kwargs={'pk': reservation.pk, 'accepte': '1'}))
        self.assertTrue(Reservation.objects.get(caracolien__user__username='a').accepte)
        email_manager = mail.outbox[-1]
        email_user = mail.outbox[-2]
        self.assertEqual(email_user.to, ['a@example.org'])
        self.assertIn('grenier est désormais acceptée', email_user.body)
        self.assertIn('de a est désormais acceptée', email_manager.body)
