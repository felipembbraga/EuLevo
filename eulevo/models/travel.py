# -*- coding: utf-8 -*-

from django.contrib.gis.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from guardian.shortcuts import assign_perm

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
    destiny_description = models.CharField(max_length=200, default='')
    vehicle_type = models.IntegerField(choices=VEHICLES)
    dt_travel = models.DateField()
    blocked = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def user_point(self):
        from core.serializers import UserPointSerializer
        data = hasattr(self.owner, 'userpoint') and getattr(self.owner, 'userpoint') or None
        return UserPointSerializer(data, many=False).data


@receiver(post_save, sender=Travel)
def travel_post_save(sender, instance, created, **kwargs):
    assign_perm('change_travel', instance.owner, instance)


class TravelHistory(models.Model):
    user = models.ForeignKey(CoreUser)
    travel = models.ForeignKey(Travel)
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=False)
    deals = models.ManyToManyField('Deal')