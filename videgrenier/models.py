from django.db import models

from caracole.models import Caracolien


class Reservation(models.Model):
    caracolien = models.ForeignKey(Caracolien)
    accepte = models.BooleanField('accepté', default=False)

    def __str__(self):
        return str(self.caracolien)

    def prix(self):
        return 12 if self.caracolien.adherent() else 14
