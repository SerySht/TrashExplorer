# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from .models import TrashInfo, TaskInfo
from smrm import trash, trashconfig
from .forms import TrashForm, TaskForm
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


class TrashList(ListView):
    model = TrashInfo
    template_name = "TrashExplorer/index.html"

    def get_queryset(self):
        return TrashInfo.objects.all()


class AddTrash(CreateView):
    success_url = "/"
    template_name = "TrashExplorer/add_trash.html"
    model = TrashInfo
    form_class = TrashForm


class TaskList(ListView):
    model = TaskInfo
    template_name = "TrashExplorer/task_list.html"

    def get_queryset(self):
        return TaskInfo.objects.all()


class AddTask(CreateView):
    success_url = "/task_list"
    template_name = "TrashExplorer/add_task.html"
    model = TaskInfo
    form_class = TaskForm


class TrashDetails(DeleteView):
    model = TrashInfo
    template_name = 'TrashExplorer/trash_details.html'


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






def delete_trash(request, trash_id):
    trash_object = get_object_or_404(TrashInfo, id=trash_id)
    t = trash.Trash(trash_object.trash_path)
    trash_object.delete()
    t.delete_trash()
    return redirect('/')


def wipe_trash(request, trash_id):
    trash_object = get_object_or_404(TrashInfo, id=trash_id)
    t = trash.Trash(trash_object.trash_path)
    t.wipe_trash()
    return redirect('/' + trash_id +'/')








class UpdateTrash(UpdateView):
    success_url = "/"
    template_name = "TrashExplorer/update_trash.html"
    model = TrashInfo
    fields = ("trash_path", "config_path", "trash_maximum_size", "file_storage_time", "recover_conflict")
    #add_rename


def run(request, task_id):
    task = get_object_or_404(TaskInfo, id=task_id)

    t = trash.Trash(task.trash.trash_path)
    print task.operation_type
    if task.operation_type == "simple delete":
        info_message = t.delete_to_trash(task.target)
        task.info_message = info_message[0]
    else:
        if task.regex != "":
            info_message = t. delete_to_trash_by_reg(task.regex, task.target)
            task.info_message = info_message[0]
        else:
            task.info_message = "You didn't enter regex"
    task.done = True;
    task.save()
    return redirect('/task_list')


















