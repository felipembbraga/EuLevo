from core.serializers import ProfileSerializer, UserPointSerializer
from core.models import Profile
from models import UserPoint


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
    try:
        data['profile'] = ProfileSerializer(user.profile).data
    except Profile.RelatedObjectDoesNotExist:
        pass
    try:
        data['point'] = UserPointSerializer(user.userpoint).data
    except UserPoint.RelatedObjectDoesNotExist:
        pass
    finally:
        return data
