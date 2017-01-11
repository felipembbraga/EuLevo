# -*- coding: utf-8 -*-
import datetime
import random
from django.contrib.gis.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from guardian.shortcuts import assign_perm

from core.models import CoreUser

from .package import Package
from .travel import Travel
from decimal import Decimal

DEAL_STATUS_CHOICES = (
    (1, 'aberto'),
    (2, 'concluido'),
    (3, 'rejeitado'),
    (4, 'cancelado'),
    (5, 'finalizado')
)

DONE_DEAL_STATUS_CHOICES = (
    (1, 'aguardando coleta'),
    (2, 'em viagem'),
    (3, 'entregue'),
    (4, 'finalizado'),
    (5, 'contestado'),
    (6, 'deletado')
)

ROLE_CHOICES = (
    (1, 'remetente'),
    (2, 'viajante')
)

DEAL_CONTEST_STATUS_CHOICES = (
    (1, 'aberto'),
    (2, u'concluído')
)


class Deal(models.Model):
    package = models.ForeignKey(Package)
    travel = models.ForeignKey(Travel)
    user = models.ForeignKey(CoreUser)
    status = models.IntegerField(choices=DEAL_STATUS_CHOICES, default=1)
    last_value = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal(0.00))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('package', 'travel')

    def get_package(self):
        from eulevo.serializers import PackageSerializer
        return PackageSerializer(self.package, many=False).data

    def get_travel(self):
        from eulevo.serializers import TravelSerializer
        return TravelSerializer(self.travel, many=False).data


@receiver(post_save, sender=Deal)
def deal_post_save(sender, instance, created, **kwargs):
    assign_perm('change_deal', instance.travel.owner, instance)
    assign_perm('change_deal', instance.package.owner, instance)


class DoneDeal(models.Model):
    deal = models.OneToOneField(Deal)
    protocol = models.CharField(max_length=15)
    token = models.CharField(max_length=10)
    delivery_at = models.DateTimeField(null=True, blank=True)
    received_at = models.DateTimeField(null=True, blank=True)
    token_checked = models.BooleanField(default=False)
    observation = models.CharField(max_length=140, null=True, blank=True)
    status = models.IntegerField(choices=DONE_DEAL_STATUS_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def generate_protocol(deal):
        today = datetime.date.today()
        return '{0}{1}{2}{3}'.format(
            str(today.year),
            str(today.month).rjust(2, '0'),
            str(today.day).rjust(2, '0'),
            str(deal.pk).rjust(4, '0')
        )

    @staticmethod
    def generate_token():
        return ''.join([str(random.randrange(0, 10)) for i in range(10)])

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     if not self.protocol:
    #         today = datetime.date.today()
    #         self.protocol = '{0}{1}{2}{3}'.format(
    #             str(today.year),
    #             str(today.month).rjust(2,'0'),
    #             str(today.day).rjust(2, '0'),
    #             str(self.deal.pk).rjust(4)
    #         )
    #     if not self.token:
    #         self.token = ''.join([random.randrange(0,10) for i in range(10)])
    #     super(DoneDeal, self).save(force_insert, force_update, using, update_fields)

    def get_deal(self):
        from eulevo.serializers import DealSerializer
        return DealSerializer(self.deal, many=False).data


@receiver(post_save, sender=DoneDeal)
def donedeal_post_save(sender, instance, created, **kwargs):
    assign_perm('change_donedeal', instance.deal.travel.owner, instance)
    assign_perm('change_donedeal', instance.deal.package.owner, instance)


class DealContest(models.Model):
    user = models.ForeignKey(CoreUser)
    deal = models.ForeignKey(Deal)
    status = models.IntegerField(choices=DEAL_CONTEST_STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    messages = models.ManyToManyField(CoreUser, related_name='contestmessages', through='ContestMessage')


class ContestMessage(models.Model):
    user = models.ForeignKey(CoreUser)
    deal_contest = models.ForeignKey(DealContest)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Rating(models.Model):
    user = models.ForeignKey(CoreUser)
    deal = models.ForeignKey(Deal)
    role = models.IntegerField(choices=ROLE_CHOICES)
    rating = models.FloatField()

    class Meta:
        unique_together = ('user', 'deal')
