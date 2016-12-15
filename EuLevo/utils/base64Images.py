from base64 import b64decode

from django.core.files.base import ContentFile


def b64_to_image(string, name='image', mimetype='jpg'):
    image_data = b64decode(string)
    return ContentFile(image_data, '{0}.{1}'.format(name, mimetype))