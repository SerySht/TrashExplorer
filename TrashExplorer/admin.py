# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import TrashInfo, TaskInfo

admin.site.register(TrashInfo)
admin.site.register(TaskInfo)
