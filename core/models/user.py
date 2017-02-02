# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, Permission
from django.contrib.gis.db import models
from django.core.mail import send_mail
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.six import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from rest_framework_jwt.settings import api_settings
from guardian.shortcuts import assign_perm

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

SOCIAL_TYPES = (
    (1, 'google'),
    (2, 'facebook')
)

SOCIAL_TYPES_DICT = {num: value for num, value in SOCIAL_TYPES}


def profile_directory_path(instance, filename):
    """
    Função para definir o diretório onde a imagem de perfil será armazenada
    Args:
        instance: Profile
        filename: String

    Returns: String

    """
    now = datetime.datetime.now()
    return 'user_{0}/profile/{1}_{2}'.format(instance.user.id, now, filename)


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

    @property
    def point(self):
        from core.serializers import UserPointSerializer
        data = hasattr(self, 'userpoint') and getattr(self, 'userpoint') or None
        return UserPointSerializer(data, many=False, hide_user=True).data

    def social_authenticate(self, social_type=None, key=None):
        if self.sociallogin_set.filter(social_type=social_type).exists():
            try:
                self.sociallogin_set.get(social_type=social_type, key=key)
            except SocialLogin.DoesNotExist:
                return False
        else:
            self.sociallogin_set.create(key=key, social_type=social_type)
        return True

    class Meta:
        """
        """
        verbose_name = _('user')
        verbose_name_plural = _('users')


@receiver(post_save, sender=CoreUser)
def coreuser_post_save(sender, instance, created, **kwargs):
    from django.contrib.contenttypes.models import ContentType

    for ct in ContentType.objects.filter(app_label='core'):
        permissions = Permission.objects.filter(content_type=ct)
        instance.user_permissions.add(*permissions)
    for ct in ContentType.objects.filter(app_label='eulevo'):
        permissions = Permission.objects.filter(content_type=ct).filter(
            Q(codename__startswith='add') | Q(codename__startswith='change') | Q(codename__startswith='delete_packageimage'))
        instance.user_permissions.add(*permissions)


class Profile(models.Model):
    """
    """
    user = models.OneToOneField(CoreUser)
    name = models.CharField(max_length=100)
    cpf_cnpj = models.CharField(max_length=15, null=True, blank=True)
    phone = models.CharField(max_length=15, default='0000000000')
    rating = models.FloatField(default=0)
    social_image = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to=profile_directory_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


@receiver(post_save, sender=Profile)
def profile_post_save(sender, instance, created, **kwargs):
    assign_perm('change_profile', instance.user, instance)


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

    @property
    def social_name(self):
        return SOCIAL_TYPES_DICT.get(self.social_type)


class Device(models.Model):
    """
    """
    user = models.ForeignKey(CoreUser)
    gcm_key = models.CharField(max_length=255)
    enabled = models.BooleanField(default=True)

    class Meta:
        unique_together=('user', 'gcm_key')


@receiver(post_save, sender=Device)
def device_post_save(sender, instance, *args, **kwargs):
    assign_perm('change_device', instance.user, instance)
    if instance.enabled == True:
        Device.objects.filter(gcm_key=instance.gcm_key, enabled=True).exclude(pk=instance.pk).update(enabled=False)


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


@receiver(post_save, sender=UserPoint)
def userpoint_post_save(sender, instance, created, **kwargs):
    assign_perm('change_userpoint', instance.user, instance)
