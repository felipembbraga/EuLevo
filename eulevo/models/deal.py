# -*- coding: utf-8 -*-

from django.contrib.gis.db import models
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

ROLE_CHOICES =(
    (1,     'remetente'),
    (2,     'viajante')
)

DEAL_CONTEST_STATUS_CHOICES = (
    (1, 'aberto'),
    (2, u'concluído')
)


class Deal(models.Model):
    package = models.ForeignKey(Package)
    travel = models.ForeignKey(Travel)
    user = models.ForeignKey(CoreUser)
    status = models.IntegerField(choices=DEAL_STATUS_CHOICES)
    last_value = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal(0.00))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('package', 'travel')

class DoneDeal(models.Model):
    deal = models.OneToOneField(Deal)
    protocol = models.CharField(max_length=15)
    token = models.CharField(max_length=10)
    delivery_at = models.DateTimeField(null=True, blank=True)
    received_at = models.DateTimeField(null=True, blank=True)
    token_checked = models.BooleanField(default=False)
    observation = models.CharField(max_length=140)
    status = models.IntegerField(choices=DONE_DEAL_STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


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