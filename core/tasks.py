from __future__ import absolute_import

from celery import shared_task
from core.models import CoreUser, Device


@shared_task
def send_multiply_messages(pk_list=[], *args, **kwargs):
    Device.objects.filter(user__pk__in=pk_list, is_active=True).send_message(*args, **kwargs)


@shared_task
def send_single_message(pk, *args, **kwargs):
    try:
        user=CoreUser.objects.get(pk=pk)
    except CoreUser.DoesNotExist:
        return

    user.send_message(*args, **kwargs)