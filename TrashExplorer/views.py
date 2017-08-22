# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from .models import TrashInfo, TaskInfo
from smrm import trash, trashconfig
from .forms import TrashForm, TaskForm
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
import multiprocessing

#todolist
#logging
#mp join?
#file open mods
#test policy
#reg P
#perekrivanie
#log wtf
#exam tasks
#try file explorer

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


class UpdateTrash(UpdateView):
    success_url = "/"
    template_name = "TrashExplorer/update_from.html"
    model = TrashInfo
    fields = ("trash_path",  "trash_maximum_size", "file_storage_time", "rename_when_nameconflict", "log_path",)


def trash_details(request, trash_id):
    trash_object = get_object_or_404(TrashInfo, id=trash_id)
    t = trash.Trash(trash_object.trash_path)
    context = {
        "trash_id": trash_id,
        "trash_list": t.show_trash()
    }
    return render(request, 'TrashExplorer/trash_details.html', context)


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
    return redirect('/' + trash_id + '/')


def recover(request, trash_id):
    trash_object = get_object_or_404(TrashInfo,  id=trash_id)
    t = trash.Trash(trash_object.trash_path,
                    recover_conflict=trash_object.rename_when_nameconflict,
                    log_path=trash_object.log_path
                    )
    recover_list = request.POST.getlist('file')
    for f in recover_list:
        for a, b, trash_path, old_filepath in t.show_trash():
            if trash_path == f:
                t.mover_from_trash(trash_path, old_filepath)

    return redirect('/' + trash_id + '/')


###############


class TaskList(ListView):
    model = TaskInfo
    template_name = "TrashExplorer/task_list.html"

    def get_queryset(self):
        return reversed(TaskInfo.objects.all())


class AddTask(CreateView):
    success_url = "/task_list"
    template_name = "TrashExplorer/add_task.html"
    model = TaskInfo
    form_class = TaskForm


class UpdateTask(UpdateView):
    success_url ="/task_list"
    template_name = "TrashExplorer/update_from.html"
    model = TaskInfo
    fields = (
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
    )


def DeleteTask(request, task_id):
    task_object = get_object_or_404(TaskInfo, id=task_id)
    task_object.delete()
    return redirect('/task_list')


def run(request, task_id):
    task = get_object_or_404(TaskInfo, id=task_id)

    #for new parameters
    task_dict = task.__dict__
    trash_dict = task.trash.__dict__

    for key in task_dict.keys():
        if task_dict[key] is None:
            task_dict.pop(key)
    trash_dict.update(task_dict)
    t = trash.Trash(task.trash.trash_path,
                    storage_time=trash_dict["file_storage_time"],
                    trash_maximum_size=trash_dict["trash_maximum_size"],
                    log_path=trash_dict["log_path"],
                    dry_run=trash_dict["dry"],
                    force=trash_dict["force"])
    print(trash_dict["log_path"])
    if task.operation_type == "simple delete":
        info_message = t.delete_to_trash(task.target)
        task.info_message = info_message[0]
    else:
        if task.regex != "":
            print task.regex, task.target

            #return_list = t.delete_to_trash_by_reg(task.regex, task.target)
            mgr = multiprocessing.Manager()
            return_list = mgr.list()
            p = multiprocessing.Process(target=t.delete_to_trash_by_reg, args=(task.regex, task.target, return_list))
            p.start()
            p.join()

            print(return_list)
            for message in return_list:
                task.info_message = task.info_message + message +'\n'
        else:
            task.info_message = "You didn't enter regex"
    task.done = True
    task.save()
    return redirect('/task_list')


















