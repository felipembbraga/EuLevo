#-*- coding: utf-8 -*-
from __future__ import absolute_import

from celery import shared_task
from core.models import CoreUser, Device
from eulevo.models import Deal

MESSAGES = {
    'package': {
        1: {
            'title': 'Temos uma viagem para a sua encomenda',
            'body': 'Veja {0}'
        },
        2: {
            'title': 'Sua encomenda foi aceita',
            'body': 'Veja detalhes de {0}'
        },
        4: {
            'title': 'Cancelada',
            'body': 'Procure outra viagem para levar {0}'
        },
        5: {
            'title': 'Viagem finalizada',
            'body': 'Sua encomenda foi entregue'
        }
    },
    'travel': {
        1: {
            'title': 'Temos uma encomenda para sua viagem',
            'body': 'Veja a viagem para {0}'
        },
        2: {
            'title': 'Sua viagem foi aceita',
            'body': 'Veja detalhes de sua viagem para {0}'
        },
        4: {
            'title': 'Cancelada',
            'body': 'Procure outra encomenda para levar a {0}'
        }
    }
}



def get_message(type, status, data):
    message_data = MESSAGES[type][status]
    return {
        'message_title': message_data['title'],
        'message_body': message_data['body'].decode('utf-8').format(data)
    }


def mount_message(deal, user, *args, **kwargs):
    package, travel = deal.package, deal.travel
    if user.pk == package.owner.pk:
        target, type, data = travel.owner, 'travel', travel.destiny_description
    else:
        target, type, data = package.owner, 'package', package.description

    try:
        message = get_message(type, deal.status, data)
    except KeyError, e:
        return
    kwargs.update(message)
    devices = Device.objects.filter(user=target, is_active=True)
    print devices.send_message(*args, **kwargs)




@shared_task
def notify_deal(deal_pk, user_pk, *args, **kwargs):
    deal = Deal.objects.get(pk=deal_pk)
    sender = CoreUser.objects.get(pk=user_pk)
    return mount_message(deal, sender, *args, **kwargs)

