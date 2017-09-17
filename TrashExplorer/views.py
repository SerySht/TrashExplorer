# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from TrashExplorer.models import TrashInfo, TaskInfo
from smrm import trash, utils
from TrashExplorer.forms import TrashForm, TaskForm
from TrashExplorer.utils import run_task, MyLock, MyPool
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView
import os


class TrashList(ListView):
    model = TrashInfo
    template_name = "TrashExplorer/index.html"


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
              "dry_run",
              )


def trash_details(request, trash_id):
    trash_object = get_object_or_404(TrashInfo, id=trash_id)
    t = trash.Trash(trash_object.trash_path)
    context = {
        "trash_id": trash_id,
        "trash_list": t.show_trash(),
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
    return redirect('trash_details', trash_id)


def recover(request, trash_id):
    trash_object = get_object_or_404(TrashInfo, id=trash_id)
    t = trash.Trash(trash_object.trash_path,
                    recover_conflict=trash_object.rename_when_nameconflict,
                    )

    recover_list = request.POST.getlist('file')
    for f in recover_list:
        for _, _, trash_path, old_filepath in t.show_trash():
            if trash_path == f:
                t.mover_from_trash(trash_path, old_filepath)
    return redirect('trash_details', trash_id)


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
              "trash_maximum_size",
              "file_storage_time",
              )


def delete_task(request, task_id):
    task_object = get_object_or_404(TaskInfo, id=task_id)
    task_object.delete()
    return redirect('/task_list')


def run(request, task_id):
    pool = MyPool()
    lock = MyLock()
    pool.apply_async(run_task, args=(task_id, lock))
    return redirect('/task_list')


def file_explorer(request):
    current_path = os.getenv('HOME')
    req = request.POST.get('dir')

    if req is not None:
        if os.path.isdir(req):
            listdir = os.listdir(req)
            current_path = req
        else:
            # to stay in the same directory (because file was chosen)
            current_path = req[:req.rfind('/')]
            listdir = os.listdir(current_path)

    else:
        listdir = os.listdir(current_path)

    url_list = []
    for f in listdir:
        if not f.startswith("."):
            filepath = os.path.join(current_path, f)
            url_list.append((f, filepath, os.path.isdir(filepath)))
    return render(request, "TrashExplorer/file_explorer.html", {"url_list": url_list})


def add_task_from_fe(request):
    form = TaskForm(initial={"target": request.POST.get('del_dir')})
    return render(request, "TrashExplorer/add_task.html", {'form': form})
