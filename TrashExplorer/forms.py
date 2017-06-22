from django import forms

from .models import TrashInfo, TaskInfo


class TrashForm(forms.ModelForm):
    class Meta:
        model = TrashInfo
        fields = [
            "trash_path",
            "config_path",
            "trash_maximum_size",
            "file_storage_time",
            "recover_conflict"
        ]


class TaskForm(forms.ModelForm):
    class Meta:
        model = TaskInfo
        fields = [
            "trash",
            "target",
            "silent",
            "dry",
            "force"
        ]
