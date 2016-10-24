# -*- coding: utf-8 -*-
from core.exceptions import SocialUserNotFound
from .models import CoreUser


class SocialLoginBackend(object):
    @staticmethod
    def authenticate(email=None, social_type=None, key=None):
        try:
            user = CoreUser.objects.get(email=email)
        except CoreUser.DoesNotExist:
            raise SocialUserNotFound(u'usuário não encontrado')
        else:
            if user.social_authenticate(social_type, key):
                return user

    @staticmethod
    def get_user(user_id):
        try:
            return CoreUser.objects.get(pk=user_id)
        except CoreUser.DoesNotExist:
            return None