# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from .models import TrashInfo, TaskInfo
from smrm import trash, trashconfig
from .forms import TrashForm, TaskForm
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
import multiprocessing
import os


# lockov dobavit pri bd
# proccesov ogr


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
    template_name = "TrashExplorer/update_form.html"
    model = TrashInfo
    fields = ("trash_path", "trash_maximum_size", "file_storage_time", "rename_when_nameconflict", "log_path",)


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
    trash_object = get_object_or_404(TrashInfo, id=trash_id)
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
    success_url = "/task_list"
    template_name = "TrashExplorer/update_form.html"
    model = TaskInfo

    fields = ("trash",
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


def delete_task(request, task_id):
    task_object = get_object_or_404(TaskInfo, id=task_id)
    task_object.delete()
    return redirect('/task_list')


def run_mp(task_id):
    task = get_object_or_404(TaskInfo, id=task_id)
    trash_obj = get_object_or_404(TrashInfo, id=task.trash.id)

    # for apply new parameters
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

    if task.operation_type == "simple delete":
        info_message = t.delete_to_trash(task.target)
        task.info_message = info_message[0]
    else:
        if task.regex != "":
            return_list = t.delete_to_trash_by_reg(task.regex, task.target)
            for message in return_list:
                task.info_message = task.info_message + message + '\n'
        else:
            task.info_message = "You didn't enter regex"

    task.done = True
    task.is_busy = False
    task.save()

    trash_obj.is_busy = False
    trash_obj.save()


def run(request, task_id):
    task = get_object_or_404(TaskInfo, id=task_id)
    task.is_busy = True
    task.save()

    trash_obj = get_object_or_404(TrashInfo, id=task.trash.id)
    trash_obj.is_busy = True
    trash_obj.save()

    p = multiprocessing.Process(target=run_mp, args=(task_id,))
    p.start()

    return redirect('/task_list')


def file_explorer(request):
    now_path = "/home/sergey/test"  # delete

    req = request.POST.get('dir')

    if req is not None:
        if os.path.isdir(req):
            lst = os.listdir(req)
            now_path = req
        else:
            lst = os.listdir(req[:req.rfind('/')])
            now_path = req[:req.rfind('/')]
    else:
        lst = os.listdir(now_path)

    url_dict = {}
    for l in lst:
        if not l.startswith("."):
            url_dict[l] = os.path.join(now_path, l)
    return render(request, "TrashExplorer/file_explorer.html", {"url_dict": url_dict})


def add_task_from_fe(request):
    form = TaskForm(initial={"target": request.POST.get('dir_b')})
    if form.is_valid():
        form.save()

        return redirect('/task_list')

    return render(request, "TrashExplorer/add_task.html", {'form': form})
