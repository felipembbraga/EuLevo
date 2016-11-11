# -*- coding: utf-8 -*-

from django.contrib.gis.db import models
from core.models import CoreUser
import datetime

WEIGHTS = (
    (1, '0 a 5kg'),
    (2, '6 a 10kg'),
    (3, '11 a 15kg'),
    (4, '16 a 20kg'),
    (5, 'mais de 20kg')
)

def package_image_directory_path(instance, filename):
    """
    Função para definir o diretório onde as imagens de encomenda serão armazenadas
    Args:
        instance: PackageImage
        filename: String

    Returns: String

    """
    now = datetime.datetime.now()
    return 'package_{0}/{1}_{2}'.format(instance.package.id, now, filename)

class Package(models.Model):
    owner = models.ForeignKey(CoreUser)
    description = models.CharField(max_length=140)
    weight_range = models.IntegerField(choices=WEIGHTS)
    destiny = models.PointField()
    receiver_name = models.CharField(max_length=100)
    receiver_phone = models.CharField(max_length=15)
    delivery_until = models.DateField()
    closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PackageImage(models.Model):
    package = models.ForeignKey(Package)
    image = models.ImageField(upload_to=package_image_directory_path)
