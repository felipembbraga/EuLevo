# -*- coding: utf-8 -*-
from core.exceptions import SocialUserNotFound
from .models import CoreUser

class SocialLoginBackend(object):
    def authenticate(self, email=None, social_type=None, key=None):
        try:
            user = CoreUser.objects.get(email=email)
        except CoreUser.DoesNotExist:
            raise SocialUserNotFound(u'usuário não encontrado')
        else:
            if user.social_authenticate(social_type, key):
                return user

    def get_user(self, user_id):
        try:
            return CoreUser.objects.get(pk=user_id)
        except CoreUser.DoesNotExist:
            return None