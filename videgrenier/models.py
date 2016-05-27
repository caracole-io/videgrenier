from django.core.urlresolvers import reverse
from django.db import models

from caracole.models import Caracolien


class Reservation(models.Model):
    caracolien = models.OneToOneField(Caracolien)
    accepte = models.NullBooleanField('accepté', default=None)
    birthdate = models.DateField('date de naissance')
    birthplace = models.CharField('lieu de naissance', max_length=250)
    id_num = models.CharField('numéro de la pièce d’identité', max_length=100)
    id_date = models.DateField('date de délivrance de la pièce d’identité')
    id_org = models.CharField('organisme délivrant la pièce d’identité', max_length=100)
    plaque = models.CharField('numéro d’immatriculation du véhicule', max_length=20)

    def __str__(self):
        return str(self.caracolien)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        email_content = 'Bonjour,\n\nVotre réservation au vide grenier est désormais %s.\n\n' % self.status()
        if self.accepte:
            email_content += 'Il ne vous reste plus qu’à envoyer un chèque de 14€ (12€ pour les adhérents).\n\n'
        email_content += 'L’équipe Caracole.'
        email_content += '\n\n--\n  Ce mail est automatique. Pour nous contacter, association.caracole@gmail.com'
        self.caracolien.user.email_user('[Caracole][Vide Grenier] Votre réservation', email_content)

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

    def profil_complete(self):
        caracolien = self.caracolien
        return all(bool(info) for info in (caracolien.user.first_name, caracolien.user.last_name, caracolien.address))
