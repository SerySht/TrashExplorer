"""Module with some utils which is used in views"""
from smrm import trash
import multiprocessing
from django.shortcuts import get_object_or_404
from TrashExplorer.models import TrashInfo, TaskInfo
from multiprocessing.pool import ThreadPool


def singleton(cls):
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance


@singleton
class MyLock(object):
    lock = multiprocessing.Lock()

    def __call__(self, args):
        return self.lock

    def __enter__(self):
        return self.lock.__enter__()

    def __exit__(self, type, value, traceback):
        self.lock.__exit__(type, value, traceback)


@singleton
class MyPool(object):
    pool = ThreadPool(processes=multiprocessing.cpu_count())

    def __call__(self, args):
        return self.pool

    def apply_async(self, target, args):
        self.pool.apply_async(target, args=args)


def run_task(task_id, lock):
    task_obj = get_object_or_404(TaskInfo, id=task_id)
    trash_obj = get_object_or_404(TrashInfo, id=task_obj.trash.id)

    if task_obj.is_busy is False and trash_obj.is_busy is False:
        task_obj.is_busy = True
        trash_obj.is_busy = True

        with lock:
            trash_obj.save()
            task_obj.save()

        task_dict = task_obj.__dict__
        for key, value in task_dict.items():
            if value is None:
                del task_dict[key]

        trash_dict = {}
        trash_dict.update(trash_obj.__dict__)
        trash_dict.update(task_dict)

        t = trash.Trash(task_obj.trash.trash_path,
                        storage_time=trash_dict["file_storage_time"],
                        trash_maximum_size=trash_dict["trash_maximum_size"],
                        dry_run=trash_dict["dry_run"],
                        verbose=True
                        )

        if task_obj.operation_type == "simple delete":
            targets = task_obj.target.splitlines()

            return_list = t.delete_to_trash(targets)
            for info_message, _ in return_list:
                task_obj.info_message += "\n" + info_message
        else:

            if task_obj.regex != "":
                return_list = t.delete_to_trash_by_reg(task_obj.regex, task_obj.target)

                for info_message, _ in return_list:
                    task_obj.info_message += "\n" + info_message
            else:
                task_obj.info_message = "You didn't enter regex"

        task_obj.is_done = True
        task_obj.is_busy = False
        trash_obj.is_busy = False

        with lock:
            trash_obj.save()
            task_obj.save()
