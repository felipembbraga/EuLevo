# -*- coding: utf-8 -*-

from django.contrib.gis.db import models
from core.models import CoreUser
from .package import WEIGHTS

VEHICLES = (
    (1, 'Carro de passeio'),
    (2, 'Caminhonete'),
    (3, 'Moto'),
    (4, u'Caminhão'),
    (5, u'Ônibus'),
    (6, u'Avião'),
    (7, 'Navio')
)

class Travel(models.Model):
    owner = models.ForeignKey(CoreUser)
    weight_range = models.IntegerField(choices=WEIGHTS)
    destiny = models.PointField()
    vehicle_type = models.IntegerField(choices=VEHICLES)
    dt_travel = models.DateField()
    blocked = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TravelHistory(models.Model):
    user = models.ForeignKey(CoreUser)
    travel = models.ForeignKey(Travel)
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=False)
    deals = models.ManyToManyField('Deal')