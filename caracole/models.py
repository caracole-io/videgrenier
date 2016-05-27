from datetime import date, timedelta

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models


class Caracolien(models.Model):
    user = models.OneToOneField(User)
    phone_regex = RegexValidator(regex=r'^\+\d{9,15}$')
    phone_number = models.CharField('téléphone', max_length=16, validators=[phone_regex], blank=True)
    adhesion = models.DateField('Date d’adhésion', blank=True, null=True,
                                help_text='les dates doivent être au format JJ/MM/AAAA')
    address = models.TextField('adresse complète', blank=True)

    def __str__(self):
        return str(self.user)

    def adherent(self):
        return bool(self.adhesion and date.today() - self.adhesion < timedelta(days=365))


def create_caracolien(sender, instance, created, **kwargs):
    if created:
        Caracolien.objects.create(user=instance)

models.signals.post_save.connect(create_caracolien, sender=User, weak=False, dispatch_uid='create_caracolien')
