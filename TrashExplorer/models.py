# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

class TrashInfo(models.Model):
    trash_name = models.CharField(max_length=200)  
    trash_config = models.CharField(max_length=200)  
