# def jwt_payload_handler(user):
#     payload = {
#         'user_id': user.pk,
#         'email': user.email,
#         'username': username,
#         'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
#     }
#     if isinstance(user.pk, uuid.UUID):
#         payload['user_id'] = str(user.pk)
#
#     payload[username_field] = username
#
#     # Include original issued at time for a brand new token,
#     # to allow token refresh
#     if api_settings.JWT_ALLOW_REFRESH:
#         payload['orig_iat'] = timegm(
#             datetime.utcnow().utctimetuple()
#         )
#
#     if api_settings.JWT_AUDIENCE is not None:
#         payload['aud'] = api_settings.JWT_AUDIENCE
#
#     if api_settings.JWT_ISSUER is not None:
#         payload['iss'] = api_settings.JWT_ISSUER
#
#     return payload