from datetime import date, timedelta

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Caracolien(models.Model):
    user = models.OneToOneField(User)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$')  # TODO: clean phone 0→+33, strip spaces, points, etc.
    phone_number = models.CharField('téléphone', max_length=16, validators=[phone_regex], blank=True)
    adhesion = models.DateField('Date d’adhésion', blank=True, null=True)
    address = models.TextField(blank=True)

    def adherent(self):
        return self.adhesion and date.today() - self.adhesion < timedelta(days=365)
