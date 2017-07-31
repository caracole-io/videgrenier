# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def insert_sites(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    Site.objects.all().update(domain='caracole.io', name='Caracole')


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_caracole_ttw'),
    ]

    operations = [
        migrations.RunPython(insert_sites),
    ]
