from __future__ import unicode_literals

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator, ASCIIUsernameValidator
from django.core.mail import send_mail
from django.db import models
from django.utils import six
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from EuLevo.mixins import AuditedMixin


class CoreUser(models.Model, AuditedMixin):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(null=True, blank=True)
    is_enabled = models.BooleanField(default=True)
    is_locked = models.BooleanField(default=False)
    email_confirmated = models.BooleanField(default=False)
    token = models.CharField(max_length=100)
    friends = models.ManyToManyField("self")


