# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-30 13:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_device_active'),
    ]

    operations = [
        migrations.RenameField(
            model_name='device',
            old_name='active',
            new_name='enabled',
        ),
    ]
