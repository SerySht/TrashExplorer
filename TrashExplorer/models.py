# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.validators import MaxValueValidator
from django.db import models
import os


class TrashInfo(models.Model):
    trash_path = models.CharField(max_length=200, unique=True)
    trash_maximum_size = models.IntegerField(default=200000,  validators=[MaxValueValidator(2147483645)])
    file_storage_time = models.IntegerField(default=7, validators=[MaxValueValidator(2147483645)])
    rename_when_nameconflict = models.BooleanField(default=True)
    log_path = models.CharField(max_length=500, default=os.path.join(os.getenv('HOME'), 'smrm.log'))
    silent = models.BooleanField(default=False)
    dry_run = models.BooleanField(default=False)
    is_busy = models.BooleanField(default=False)

    def __unicode__(self):
        return os.path.basename(self.trash_path)


class TaskInfo(models.Model):
    trash = models.ForeignKey(TrashInfo)
    target = models.TextField()
    silent = models.BooleanField()
    dry_run = models.BooleanField()

    OPERATION_CHOICES = (
        ("simple delete", "simple delete"),
        ("delete by regex", "delete by regex"),
    )
    operation_type = models.CharField(max_length=50, choices=OPERATION_CHOICES)

    info_message = models.TextField(max_length=300)
    regex = models.CharField(max_length=200, blank=True, null=True)
    trash_maximum_size = models.IntegerField(blank=True, null=True, validators=[MaxValueValidator(2147483645)])
    file_storage_time = models.IntegerField(blank=True, null=True, validators=[MaxValueValidator(2147483645)])
    log_path = models.CharField(max_length=500, blank=True, null=True)
    is_busy = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)

    def __unicode__(self):
        return os.path.basename(self.target)
