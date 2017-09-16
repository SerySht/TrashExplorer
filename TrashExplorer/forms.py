# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from .models import TrashInfo, TaskInfo


class TrashForm(forms.ModelForm):
    class Meta:
        model = TrashInfo
        fields = [
            "trash_path",
            "rename_when_nameconflict",
            "log_path",
            "trash_maximum_size",
            "file_storage_time",
            "silent",
            "dry_run"
        ]


class TaskForm(forms.ModelForm):
    class Meta:
        model = TaskInfo
        fields = [
            "trash",
            "operation_type",
            "target",
            "regex",
            "silent",
            "dry_run",
            "log_path",
            "trash_maximum_size",
            "file_storage_time",
        ]
