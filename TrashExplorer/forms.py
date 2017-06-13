from django import forms

from .models import TrashInfo


class TrashForm(forms.ModelForm):
    class Meta:
        model = TrashInfo
        fields = [
            "trash_name",
            "trash_path"
        ]
