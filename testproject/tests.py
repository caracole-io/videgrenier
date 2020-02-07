"""Main test module."""
from datetime import date, timedelta
from random import randint
from typing import Any, Dict

from django.conf import settings
from django.contrib.auth.models import Group, User
from django.core import mail
from django.template.defaultfilters import date as date_filter
from django.test import TestCase
from django.urls import reverse

from videgrenier.models import Reservation


def infos(guy: str) -> Dict[str, Any]:
    """Generate an account for a guy."""
    birthdate = date(1970, 1, 1) + timedelta(days=randint(1, int(1E4)))
    age = (date.today() - birthdate).days
    return {
        'birthdate': birthdate,
        'birthplace': f'birthplace of {guy}',
        'id_num': f'id number of {guy}',
        'id_date': date.today() - timedelta(days=randint(1, age)),
        'id_org': f'id issuer of {guy}',
        'plaque': f'plaque of {guy}',
        'address': f'address of {guy}',
    }


class VideGrenierTests(TestCase):
    """Main test class."""
    def setUp(self):
        """Create a few guys and an Adherent group."""
        adherents = Group.objects.create(name='adherents')
        for guy in 'abcd':
            user = User.objects.create_user(guy, email='%s@example.org' % guy, password=guy)
            if guy == 'a':
                user.first_name = 'a'
                user.last_name = 'a'
                user.groups.add(adherents)
                user.save()
                Reservation.objects.create(user=user, **infos(guy))
            elif guy == 'b':
                Reservation.objects.create(user=user, **infos(guy))
            elif guy == 'd':
                user.is_staff = True
                user.save()

    # MODELS

    def test_reservation_prix(self):
        """Test price computation for the different guys."""
        for reservation in Reservation.objects.all():
            self.assertEqual(reservation.prix(), 12 if str(reservation) == 'a' else 14)

    # VIEWS

    def test_views_status(self):
        """Test login and access."""
        self.client.login(username='c', password='c')
        self.client.login(username='a', password='a')
        self.assertEqual(self.client.get(reverse('videgrenier:reservation-detail')).status_code, 200)
        self.assertEqual(self.client.get(reverse('videgrenier:reservation')).status_code, 200)
        self.assertEqual(self.client.get(reverse('videgrenier:reservation-delete')).status_code, 200)

    def test_reservation_update_view(self):
        """Test reselvation updates ."""
        reservation = Reservation.objects.get(user__username='a')
        self.assertIsNone(reservation.accepte)
        self.client.login(username='d', password='d')  # d est staff

        # la réservation vient d’être créée, gros mail
        email_user = mail.outbox[-1]
        self.assertEqual(email_user.to, ['a@example.org'])
        self.assertIn('Vous avez effectué une demande d’inscription', email_user.body)

        # d refuse la réservation: la réservation est refusée, a & c reçoivent des mails correspondants
        self.client.get(reverse('videgrenier:reservation-moderate', kwargs={'pk': reservation.pk, 'accepte': 0}))
        self.assertFalse(Reservation.objects.get(user__username='a').accepte)
        email_user = mail.outbox[-1]
        self.assertEqual(email_user.to, ['a@example.org'])
        self.assertIn('grenier est désormais refusée', email_user.body)

        # d accept la réservation: la réservation est acceptée, a & c reçoivent des mails correspondants
        self.client.get(reverse('videgrenier:reservation-moderate', kwargs={'pk': reservation.pk, 'accepte': 1}))
        self.assertTrue(Reservation.objects.get(user__username='a').accepte)
        email_user = mail.outbox[-1]
        self.assertEqual(email_user.to, ['a@example.org'])
        self.assertIn('grenier est désormais acceptée', email_user.body)

    # Dates

    def test_dates(self):
        """Test opening / closing dates."""
        self.assertLess(settings.DATES_VIDE_GRENIER['open'], settings.DATES_VIDE_GRENIER['close'])
        self.assertLess(settings.DATES_VIDE_GRENIER['close'], settings.DATES_VIDE_GRENIER['event'])
        for status in ['open', 'close', 'event']:
            self.assertIn(date_filter(settings.DATES_VIDE_GRENIER[status], 'j F o'),
                          self.client.get(reverse('videgrenier:home')).content.decode())
