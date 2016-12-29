# -*- coding: utf-8 -*-

from django.contrib.gis.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from guardian.shortcuts import assign_perm

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
    return 'user_{0}/package_{1}/{2}_{3}'.format(
        instance.package.owner.id,
        instance.package.id,
        now,
        filename)

class Package(models.Model):
    owner = models.ForeignKey(CoreUser)
    description = models.CharField(max_length=140)
    weight_range = models.IntegerField(choices=WEIGHTS)
    destiny = models.PointField()
    destiny_description = models.CharField(max_length=200, default='')
    receiver_name = models.CharField(max_length=100)
    receiver_phone = models.CharField(max_length=15)
    delivery_until = models.DateField()
    closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def package_images(self):
        from eulevo.serializers import PackageImageSerializer
        package_images = self.packageimage_set.all()
        return PackageImageSerializer(package_images, many=True).data

    @property
    def user_point(self):
        from core.serializers import UserPointSerializer
        data = hasattr(self.owner, 'userpoint') and getattr(self.owner, 'userpoint') or None
        return UserPointSerializer(data, many=False).data


@receiver(post_save, sender=Package)
def package_post_save(sender, instance, created, **kwargs):

    assign_perm('change_package', instance.owner, instance)


class PackageImage(models.Model):
    package = models.ForeignKey(Package)
    image = models.ImageField(upload_to=package_image_directory_path)


@receiver(post_save, sender=PackageImage)
def packageimage_post_save(sender, instance, created, **kwargs):
    assign_perm('change_packageimage', instance.package.owner, instance)
    assign_perm('delete_packageimage', instance.package.owner, instance)

