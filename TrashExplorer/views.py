# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from .models import TrashInfo, TaskInfo
from smrm import trash, trashconfig
from .forms import TrashForm, TaskForm
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
import multiprocessing
import os


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

lock = multiprocessing.Lock()


def run_mp(task_obj, trash_obj):
    task_dict = task_obj.__dict__
    trash_dict = {}
    trash_dict.update(trash_obj.__dict__)
    trash_dict.update(task_dict)

    t = trash.Trash(task_obj.trash.trash_path,
                    storage_time=trash_dict["file_storage_time"],
                    trash_maximum_size=trash_dict["trash_maximum_size"],
                    log_path=trash_dict["log_path"],
                    dry_run=trash_dict["dry"],
                    force=trash_dict["force"])

    if task_obj.operation_type == "simple delete":
        info_message = t.delete_to_trash(task_obj.target)
        task_obj.info_message = info_message[0]
    else:
        if task_obj.regex != "":
            return_list = t.delete_to_trash_by_reg(task_obj.regex, task_obj.target)
            for message in return_list:
                task_obj.info_message = task_obj.info_message + message + '\n'
        else:
            task_obj.info_message = "You didn't enter regex"

    task_obj.done = True
    task_obj.is_busy = False
    trash_obj.is_busy = False
    lock.acquire()
    trash_obj.save()
    task_obj.save()
    lock.release()


def run(request, task_id):
    task_obj = get_object_or_404(TaskInfo, id=task_id)
    task_obj.is_busy = True
    trash_obj = get_object_or_404(TrashInfo, id=task_obj.trash.id)
    trash_obj.is_busy = True

    lock.acquire()
    trash_obj.save()
    task_obj.save()
    lock.release()

    p = multiprocessing.Process(target=run_mp, args=(task_obj, trash_obj))
    p.start()

    return redirect('/task_list')


def file_explorer(request):
    current_path = os.getenv('HOME')
    req = request.POST.get('dir')

    if req is not None:
        if os.path.isdir(req):
            lst = os.listdir(req)
            current_path = req
        else:
            lst = os.listdir(req[:req.rfind('/')])
            current_path = req[:req.rfind('/')]
    else:
        lst = os.listdir(current_path)

    url_dict = {}
    for l in lst:
        if not l.startswith("."):
            url_dict[l] = os.path.join(current_path, l)
    return render(request, "TrashExplorer/file_explorer.html", {"url_dict": url_dict})


def add_task_from_fe(request):
    form = TaskForm(initial={"target": request.POST.get('del_dir')})
    if form.is_valid():
        form.save()
        return redirect('/task_list')
    return render(request, "TrashExplorer/add_task.html", {'form': form})
