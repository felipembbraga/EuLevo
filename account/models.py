from __future__ import unicode_literals

from django.contrib.gis.db import models

# Create your models here.


class Revenue(models.Model):
    description = models.CharField(max_length=150)

