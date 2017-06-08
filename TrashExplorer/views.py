# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from .models import TrashInfo
from smrm import trash


def home(request):
    trashes = TrashInfo.objects.all()
    return render(request, 'TrashExplorer/home.html', {"trashes":trashes})


def trash_deatils(request, trash_name):
    trash_object = get_object_or_404(TrashInfo, trash_name = trash_name)
    trash_path = trash_object.trash_config
    t = trash.Trash(trash_path)
    trash_list = t.show_trash(0)
    print trash_name
    return render(request, 'TrashExplorer/detail.html', {"trash_name": trash_name,"filelist":trash_list })


def recover(request, trash_name):
    trash_object = get_object_or_404(TrashInfo, trash_name=trash_name)
    trash_path = trash_object.trash_config
    t = trash.Trash(trash_path)
    tup = request.POST['trash']
    trash_list = t.show_trash(0)
    tup2 = ""
    for i in trash_list:
        if i[0] == tup:
            tup2 = i[1]
    print '------------------', tup, ' ', tup2
    t.mover_from_trash(tup, tup2)
    trash_list2 = t.show_trash(0)
    return render(request, 'TrashExplorer/detail.html', {"trash_name": trash_name,"filelist": trash_list2})