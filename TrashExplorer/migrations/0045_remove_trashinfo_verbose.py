# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-14 23:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TrashExplorer', '0044_remove_taskinfo_k'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trashinfo',
            name='verbose',
        ),
    ]