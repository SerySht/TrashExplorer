from smrm import trash
import multiprocessing
from django.shortcuts import get_object_or_404
from TrashExplorer.models import TrashInfo, TaskInfo

lock = multiprocessing.Lock()


def run_task(task_id):

    task_obj = get_object_or_404(TaskInfo, id=task_id)
    task_obj.is_busy = True
    trash_obj = get_object_or_404(TrashInfo, id=task_obj.trash.id)
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
                    log_path=trash_dict["log_path"],
                    dry_run=trash_dict["dry_run"],
                    force=trash_dict["force"],
                    verbose=task_dict["verbose"]
                    )

    if task_obj.operation_type == "simple delete":
        targets = task_obj.target.split()
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

    task_obj.done = True
    task_obj.is_busy = False
    trash_obj.is_busy = False

    with lock:
        trash_obj.save()
        task_obj.save()
