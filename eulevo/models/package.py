# -*- coding: utf-8 -*-

from django.contrib.gis.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from guardian.shortcuts import assign_perm

from core.models import CoreUser, Profile
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
    import hashlib
    user_folder = hashlib.new('md5', 'user_{0}'.format(instance.package.owner.id)).hexdigest()
    package_folder = hashlib.new('md5', 'package_{0}'.format(instance.package.id)).hexdigest()
    now = datetime.datetime.now()
    filename = '{0}_{1}'.format(now, filename)
    return '{0}/{1}/{2}'.format(user_folder, package_folder, filename)


class Package(models.Model):
    """
    """
    owner = models.ForeignKey(CoreUser)
    description = models.CharField(max_length=140)
    weight_range = models.IntegerField(choices=WEIGHTS)
    destiny = models.PointField()
    destiny_description = models.CharField(max_length=200, default='')
    receiver_name = models.CharField(max_length=100)
    receiver_phone = models.CharField(max_length=15)
    # delivery_until = models.DateField()
    closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def package_images(self):
        """

        Returns:

        """
        from eulevo.serializers import PackageImageSerializer
        package_images = self.packageimage_set.all()
        return PackageImageSerializer(package_images, many=True).data

    @property
    def user_point(self):
        """

        Returns:

        """
        from core.serializers import UserPointSerializer
        data = hasattr(self.owner, 'userpoint') and getattr(self.owner, 'userpoint') or None
        return UserPointSerializer(data, many=False).data

    def deals(self):
        """

        Returns:

        """
        from eulevo.serializers import DealSerializer
        deals = self.deal_set.all()
        return DealSerializer(deals, many=True).data

    def count_deals(self):
        if self.deal_set.filter(donedeal__isnull=False).exists():
            return 0
        return self.deal_set.filter(status=1).count()

    def has_donedeal(self):
        return self.deal_set.filter(donedeal__isnull=False).exists()

    def get_travel(self):
        deal = self.deal_set.filter(donedeal__isnull=False).first()
        if deal:
            from eulevo.serializers import TravelSoftSerializer
            return TravelSoftSerializer(deal.travel, many=False).data

    def get_user(self):
        donedeal = self.deal_set.filter(donedeal__isnull=False).exists()
        if donedeal:
            from core.serializers import ProfileSerializer
            return ProfileSerializer(self.owner.profile, many=False).data


@receiver(post_save, sender=Package)
def package_post_save(sender, instance, created, **kwargs):
    """

    Args:
        sender:
        instance:
        created:
        kwargs:
    """
    assign_perm('change_package', instance.owner, instance)


class PackageImage(models.Model):
    """
    """
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=package_image_directory_path)

    def delete(self, *args, **kwargs):
        """

        Args:
            args:
            kwargs:
        """
        # You have to prepare what you need before delete the model
        storage, name = self.image.storage, self.image.name
        # Delete the model before the file
        super(PackageImage, self).delete(*args, **kwargs)
        # Delete the file after the model
        storage.delete(name)


@receiver(post_save, sender=PackageImage)
def packageimage_post_save(sender, instance, created, **kwargs):
    """

    Args:
        sender:
        instance:
        created:
        kwargs:
    """
    assign_perm('change_packageimage', instance.package.owner, instance)
    assign_perm('delete_packageimage', instance.package.owner, instance)
