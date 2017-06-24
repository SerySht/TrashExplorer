# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from smrm import trashconfig
import os


class TrashInfo(models.Model):
    trash_path = models.CharField(max_length=200, unique=True)
    trash_maximum_size = models.IntegerField(default=20000)
    file_storage_time = models.IntegerField(default=7)
    rename_when_nameconflict = models.BooleanField(default=True)
    log_path = models.CharField(max_length=500, default=os.path.join(os.getenv('HOME'), 'smrm.log'))

    def __str__(self):
        return os.path.basename(self.trash_path)


class TaskInfo(models.Model):
    trash = models.ForeignKey(TrashInfo, default=None)
    target = models.CharField(max_length=500, default=" ")
    silent = models.BooleanField(default=False)
    dry = models.BooleanField(default=False)
    force = models.BooleanField(default=False)

    OPERATION_CHOICES = (
        ("simple delete", "simple delete"),
        ("delete by regex", "delete by regex"),
    )
    operation_type = models.CharField(max_length=50, choices=OPERATION_CHOICES, default=None)
    done = models.BooleanField(default=False)
    info_message = models.CharField(max_length=300, default=" ")
    regex = models.CharField(max_length=200, default=" ")
    trash_maximum_size = models.IntegerField(default=2000)
    file_storage_time = models.IntegerField(default=7)
    log_path = models.CharField(max_length=500, default=os.path.join(os.getenv('HOME'), 'smrm.log'))

    def __str__(self):
        return os.path.basename(self.target)