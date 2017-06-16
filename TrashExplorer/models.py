# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from smrm import trashconfig
import os


class TrashInfo(models.Model):
    trash_path = models.CharField(max_length=200)
    config_path = models.CharField(max_length=500, default=trashconfig.get_default_path())

    def __str__(self):
        return os.path.basename(self.trash_path)


