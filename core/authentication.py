from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.utils.translation import ugettext as _
from rest_framework import exceptions
from .models import CoreUser


class EuLevoJSONWebTokenAuthentication(JSONWebTokenAuthentication):

    def authenticate(self, request):
        raise Exception(request)
        return super(EuLevoJSONWebTokenAuthentication, self).authenticate(request)

    def authenticate_credentials(self, payload):
        """
        Returns an active user that matches the payload's user id and email.
        """

        email = payload.get('email')

        if not email:
            msg = _('Invalid payload.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = CoreUser.objects.get_by_natural_key(email)
        except CoreUser.DoesNotExist:
            msg = _('Invalid signature.')
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = _('User account is disabled.')
            raise exceptions.AuthenticationFailed(msg)

        return user