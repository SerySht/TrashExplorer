# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from .models import TrashInfo
from smrm import trash  #kekes


def home(request):
    trashes = TrashInfo.objects.all()
    return render(request, 'TrashExplorer/index.html', {"trashes": trashes})


def trash_details(request, trash_name):
    trash_object = get_object_or_404(TrashInfo, trash_name=trash_name)
    t = trash.Trash(trash_object.trash_path)
    trash_list = t.show_trash(0)
    return render(request, 'TrashExplorer/trash_details.html', {"trash_name": trash_name, "filelist": trash_list})


def recover(request, trash_name):
    trash_object = get_object_or_404(TrashInfo, trash_name=trash_name)
    t = trash.Trash(trash_object.trash_path)
    for i in t.show_trash(0):
        if i[0] == request.POST['file']:
            old_filepath = i[1]

    t.mover_from_trash(request.POST['file'],  old_filepath)
    return render(request, 'TrashExplorer/trash_details.html', {"trash_name": trash_name, "filelist": t.show_trash(0)})


def delete(request, trash_name):
    trash_object = get_object_or_404(TrashInfo, trash_name=trash_name)
    t = trash.Trash(trash_object.trash_path)
    t.delete_to_trash([request.POST['delete']])
    return render(request, 'TrashExplorer/trash_details.html', {"trash_name": trash_name, "filelist": t.show_trash(0)})



























