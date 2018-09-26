from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.validators import RegexValidator
from django.db import models
from django.template.loader import get_template
from django.urls import reverse


class Reservation(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    accepte = models.NullBooleanField('accepté', default=None)
    birthdate = models.DateField('date de naissance')
    birthplace = models.CharField('lieu de naissance', max_length=250)
    id_num = models.CharField('numéro de la pièce d’identité', max_length=100)
    id_date = models.DateField('date de délivrance de la pièce d’identité')
    id_org = models.CharField('organisme délivrant la pièce d’identité', max_length=100)
    plaque = models.CharField('numéro d’immatriculation du véhicule', max_length=20)
    emplacements = models.IntegerField('nombre d’emplacements demandés', default=1)
    nature = models.CharField('nature des objets exposés', max_length=250, default='')

    phone_regex = RegexValidator(regex=r'^[+0]\d{9,15}$')
    phone_number = models.CharField('téléphone', max_length=16, validators=[phone_regex], blank=True)
    address = models.TextField('adresse complète', blank=True)

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.accepte is None:
            if self.profil_complete():
                ctx = {'reservation': self}
                text, html = (get_template('videgrenier/mail.%s' % alt).render(ctx) for alt in ['txt', 'html'])
                msg = EmailMultiAlternatives(
                    '[Vide Grenier] Votre réservation',
                    text,
                    settings.DEFAULT_FROM_EMAIL, [self.user.email],
                    reply_to=(settings.REPLY_TO, ))
                msg.attach_alternative(html, 'text/html')
                msg.send()
        else:
            email_content = 'Bonjour,\n\nVotre réservation au vide grenier est désormais %s.\n\n' % self.status()
            email_content += 'L’équipe Caracole.'
            email_content += '\n\n--\n  Ce mail est automatique. Pour nous contacter, utilisez %s' % settings.REPLY_TO
            self.user.email_user('[Caracole][Vide Grenier] Votre réservation', email_content)

    def get_absolute_url(self):
        return reverse('videgrenier:reservation-detail')

    def prix(self):
        return 12 if self.user.groups.filter(name='adherents').exists() else 14

    def status(self):
        if self.accepte is None:
            return 'en attente de traitement'
        if self.accepte:
            return 'acceptée'
        return 'refusée'

    def profil_complete(self):
        return all(bool(info) for info in (self.user.first_name, self.user.last_name, self.address))
