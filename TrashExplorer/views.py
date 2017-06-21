# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from .models import TrashInfo
from smrm import trash, trashconfig
from .forms import TrashForm, TaskForm
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


def home(request):
    trashes = TrashInfo.objects.all()
    context = {
        "trashes": trashes
    }
    return render(request, 'TrashExplorer/index.html', context)


def trash_details(request, trash_id):
    trash_object = get_object_or_404(TrashInfo, id=trash_id)
    config = trashconfig.load(trash_object.config_path)
    config.pop("silent")
    config.pop("log_path")
    config["trash_path"] = trash_object.trash_path
    t = trash.Trash(**config)

    context = {
        "trash_id": trash_id,
        "trash_list": t.show_trash()
    }
    return render(request, 'TrashExplorer/trash_details.html', context)


def recover(request, trash_id):
    trash_object = get_object_or_404(TrashInfo,  id=trash_id)
    t = trash.Trash(trash_object.trash_path)
    recover_list = request.POST.getlist('file')
    for f in recover_list:
        for a, b, trash_path, old_filepath in t.show_trash():
            if trash_path == f:
                t.mover_from_trash(trash_path, old_filepath)

    return redirect('/' + trash_id + '/')


def delete(request, trash_id):
    trash_object = get_object_or_404(TrashInfo,  id=trash_id)
    t = trash.Trash(trash_object.trash_path)
    t.delete_to_trash(request.POST['delete'])
    return redirect('/'+trash_id +'/')



def delete_by_regex(request, trash_id):
    trash_object = get_object_or_404(TrashInfo, id=trash_id)
    t = trash.Trash(trash_object.trash_path)
    t.delete_to_trash_by_reg(request.POST['regex'], request.POST['directory'])
    return redirect('/' + trash_id + '/')




def add_trash(request):
    form = TrashForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect('/')

    context = {
         "form": form,
    }
    return render(request, "TrashExplorer/add_trash.html", context)


def delete_trash(request, trash_id):
    trash_object = get_object_or_404(TrashInfo, id=trash_id)
    t = trash.Trash(trash_object.trash_path)
    trash_object.delete()
    print t.trash_path
    t.delete_trash()
    trashes = TrashInfo.objects.all()
    return redirect('/')


def wipe_trash(request, trash_id):
    trash_object = get_object_or_404(TrashInfo, id=trash_id)
    t = trash.Trash(trash_object.trash_path)
    t.wipe_trash()
    return redirect('/'+trash_id +'/')


def add_task(request):
    form = TaskForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect('/')

    context = {
        "form": form,
    }
    return render(request, "TrashExplorer/add_task.html", context)


def task_list(request):
    return render(request, "TrashExplorer/task_list.html")


class UpdateTrash(UpdateView):
    success_url = reverse_lazy('home')
    template_name = "TrashExplorer/update_trash.html"
    model = TrashInfo
    fields = ("trash_path", "config_path", "trash_maximum_size", "file_storage_time", "recover_conflict")


class AddTrash(CreateView):
    success_url = reverse_lazy('home')
    template_name = "TrashExplorer/add_trash.html"
    model = TrashInfo
    form_class = TrashForm



















