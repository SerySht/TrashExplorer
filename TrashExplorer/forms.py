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
        ]


class TaskForm(forms.ModelForm):
    regex = forms.CharField(required=False)
    class Meta:
        model = TaskInfo
        fields = [
            "trash",
            "target",
            "operation_type",
            "regex",
            "silent",
            "dry",
            "force",
            "log_path",
            "trash_maximum_size",
            "file_storage_time",
        ]
