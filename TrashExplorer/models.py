# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from smrm import trashconfig
import os


class TrashInfo(models.Model):
    trash_path = models.CharField(max_length=200, unique=True)
    config_path = models.CharField(max_length=500, default=trashconfig.get_default_path())
    trash_maximum_size = models.IntegerField(default=200)
    file_storage_time = models.IntegerField(default=7)
    recover_conflict = models.BooleanField(default=False)

    def __str__(self):
        return os.path.basename(self.trash_path)


class TaskInfo(models.Model):
    target = models.CharField(max_length=500, default=" ")
    silent = models.BooleanField(default=False)
    dry = models.BooleanField(default=False)
    force = models.BooleanField(default=False)
