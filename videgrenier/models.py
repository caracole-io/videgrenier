from django.conf import settings
from django.core.mail import mail_managers
from django.core.urlresolvers import reverse
from django.db import models

from caracole.models import Caracolien


class Reservation(models.Model):
    caracolien = models.OneToOneField(Caracolien)
    accepte = models.NullBooleanField('accepté', default=None)

    def __str__(self):
        return str(self.caracolien)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not settings.DEBUG:
            self.caracolien.user.email_user('[Caracole][Vide Grenier] Votre réservation', 'Bonjour,\n\n'
                                            'Votre réservation au vide grenier est désormais %s.' % self.status())
            mail_managers('[Vide Grenier] Réservation', 'Bonjour,\n\n'
                          'La réservation de %s est désormais %s.' % (self, self.status()))

    def get_absolute_url(self):
        return reverse('videgrenier:reservation-detail')

    def prix(self):
        return 12 if self.caracolien.adherent() else 14

    def status(self):
        if self.accepte is None:
            return 'en attente de traitement'
        if self.accepte:
            return 'acceptée'
        return 'refusée'
