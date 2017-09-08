# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from TrashExplorer.models import TrashInfo, TaskInfo
from smrm import trash
from TrashExplorer.forms import TrashForm, TaskForm
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
import multiprocessing
import os
from runtask import run_task


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
    fields = ("trash_path",
              "trash_maximum_size",
              "file_storage_time",
              "rename_when_nameconflict",
              "log_path",
              "dry_run",
              "verbose"
              )


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
        if TaskInfo.objects.all():
            return reversed(TaskInfo.objects.all())
        else:
            return None


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
              "dry_run",
              "force",
              "log_path",
              "trash_maximum_size",
              "file_storage_time",
              "verbose",
              )


def delete_task(request, task_id):
    task_object = get_object_or_404(TaskInfo, id=task_id)
    task_object.delete()
    return redirect('/task_list')


def run(request, task_id):

    p = multiprocessing.Process(target=run_task, args=(task_id, ))
    p.start()

    return redirect('/task_list')


def file_explorer(request):
    current_path = os.getenv('HOME')
    req = request.POST.get('dir')

    if req is not None:
        if os.path.isdir(req):
            files = os.listdir(req)
            current_path = req
        else:
            files = os.listdir(req[:req.rfind('/')])
            current_path = req[:req.rfind('/')]
    else:
        files = os.listdir(current_path)

    url_list = []
    for f in files:
        if not f.startswith("."):
            filepath = os.path.join(current_path, f)
            url_list.append((f, filepath, os.path.isdir(filepath)))
    return render(request, "TrashExplorer/file_explorer.html", {"url_list": url_list})


def add_task_from_fe(request):
    form = TaskForm(initial={"target": request.POST.get('del_dir')})
    if form.is_valid():
        form.save()
        return redirect('/task_list')
    return render(request, "TrashExplorer/add_task.html", {'form': form})
