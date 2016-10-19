# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.gis.db import models
from django.core.mail import send_mail
from django.utils.six import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

SOCIAL_TYPES = (
    (1, 'facebook'),
    (2, 'google')
)


def profile_directory_path(instance, filename):
    """
    Função para definir o diretório onde a imagem de perfil será armazenada
    Args:
        instance: Profile
        filename: String

    Returns: String

    """
    now = datetime.datetime.now()
    return 'profile_{0}/{1}_{2}'.format(instance.id, now, filename)


class CoreUserManager(BaseUserManager):
    """
    """
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        """

        Args:
            email:
            password:
            extra_fields:

        Returns:

        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """

        Args:
            email:
            password:
            extra_fields:

        Returns:

        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def get_by_natural_key(self, email):
        """

        Args:
            email:

        Returns:

        """
        return self.get(email=email)


class CoreUser(AbstractBaseUser, PermissionsMixin):
    """
    """

    email = models.EmailField(unique=True)
    password = models.CharField(_('password'), max_length=128)
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
    created = False

    USERNAME_FIELD = 'email'

    def email_user(self, subject, message, from_email=None, **kwargs):
        """

        Args:
            subject:
            message:
            from_email:
            kwargs:
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_full_name(self):
        """

        Returns:

        """
        if self.profile is not None:
            return self.profile.name
        return self.get_username()

    def get_short_name(self):
        """

        """
        self.get_full_name()

    def __str__(self):
        """

        Returns:

        """
        return self.get_full_name()

    @property
    def jwt_token(self):
        """

        Returns:

        """
        payload = jwt_payload_handler(self)
        token = jwt_encode_handler(payload)
        return token

    def full_profile(self):
        from core.serializers import ProfileSerializer
        data = hasattr(self, 'profile') and getattr(self, 'profile') or None
        return ProfileSerializer(data, many=False).data

    class Meta:
        """
        """
        verbose_name = _('user')
        verbose_name_plural = _('users')


class Profile(models.Model):
    """
    """
    user = models.OneToOneField(CoreUser)
    name = models.CharField(max_length=100)
    cpf_cnpj = models.CharField(unique=True, max_length=15, null=True, blank=True)
    rating = models.FloatField(default=0)
    social_image = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to=profile_directory_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SocialLogin(models.Model):
    """
    """
    user = models.ForeignKey(CoreUser)
    social_type = models.IntegerField(choices=SOCIAL_TYPES)
    key = models.CharField(max_length=255)

    class Meta:
        """
        """
        unique_together = ('user', 'social_type')


class Device(models.Model):
    """
    """
    user = models.ForeignKey(CoreUser)
    gcm_key = models.CharField(max_length=255)


@python_2_unicode_compatible
class UserPoint(models.Model):
    """
    """
    user = models.OneToOneField(CoreUser)
    point = models.PointField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """

        Returns:

        """
        return '{0},{1}'.format(self.point.get_y(), self.point.get_x())
