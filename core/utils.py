from core.serializers import ProfileSerializer, UserPointSerializer
from .models import Profile, UserPoint


def jwt_response_payload_handler(token, user=None, request=None):
    """
    Returns the response data for both the login and refresh views.
    Override to return a custom response such as including the
    serialized representation of the User.

    Example:

    def jwt_response_payload_handler(token, user=None, request=None):
        return {
            'token': token,
            'user': UserSerializer(user).data
        }

    """
    data = {
        'success': True,
        'token': token,
        'email': user and user.email or None
    }
    if hasattr(user, 'profile'):
        data['profile'] = ProfileSerializer(getattr(user, 'profile')).data
    if hasattr(user, 'userpoint'):
        data['point'] = UserPointSerializer(getattr(user, 'userpoint')).data
    return data
