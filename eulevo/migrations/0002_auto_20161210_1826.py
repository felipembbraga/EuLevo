# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-10 21:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('eulevo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deal',
            name='status',
            field=models.IntegerField(
                choices=[(1, b'aberto'), (2, b'concluido'), (3, b'rejeitado'), (4, b'cancelado'), (5, b'finalizado')],
                default=1),
        ),
        migrations.AlterField(
            model_name='donedeal',
            name='observation',
            field=models.CharField(blank=True, max_length=140, null=True),
        ),
        migrations.AlterField(
            model_name='donedeal',
            name='status',
            field=models.IntegerField(
                choices=[(1, b'aguardando coleta'), (2, b'em viagem'), (3, b'entregue'), (4, b'finalizado'),
                         (5, b'contestado'), (6, b'deletado')], default=1),
        ),
    ]
