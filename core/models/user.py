# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.gis.db import models
from django.core.mail import send_mail
from django.utils.six import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

SOCIAL_TYPES = (
    (1, 'facebook'),
    (2, 'google')
)


def profile_directory_path(instance, filename):
    now = datetime.datetime.now()
    return 'profile_{0}/{1}_{2}'.format(instance.id, now, filename)


class CoreUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CoreUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_enabled = models.BooleanField(_('enabled'), default=True)
    is_locked = models.BooleanField(_('locked'), default=False)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    email_confirmated = models.BooleanField(_('email confirmated'), default=False)
    token = models.CharField(max_length=100, blank=True, null=True)
    friends = models.ManyToManyField("self", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CoreUserManager()

    USERNAME_FIELD = 'email'

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_full_name(self):
        if self.profile is not None:
            return self.profile.name
        return self.get_username()

    def get_short_name(self):
        self.get_full_name()

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


class Profile(models.Model):
    user = models.OneToOneField(CoreUser)
    name = models.CharField(max_length=100)
    cpf_cnpj = models.CharField(unique=True, max_length=15, null=True, blank=True)
    rating = models.FloatField(default=0)
    social_image = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to=profile_directory_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SocialLogin(models.Model):
    user = models.ForeignKey(CoreUser)
    social_type = models.IntegerField(choices=SOCIAL_TYPES)
    key = models.CharField(max_length=255)

    class Meta:
        unique_together = ('user', 'social_type')


class Device(models.Model):
    user = models.ForeignKey(CoreUser)
    gcm_key = models.CharField(max_length=255)


@python_2_unicode_compatible
class UserPoint(models.Model):
    user = models.OneToOneField(CoreUser)
    point = models.PointField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{0},{1}'.format(self.point.get_y(), self.point.get_x())
