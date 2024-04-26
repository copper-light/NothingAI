import threading
from apps.training.models import TaskQueue as TaskQueueDB
from django.db.models import Q

# class TaskQueue:
#
#     def __init__(self):
#         self.lock = threading.RLock()
#         self.q = []
#
#     def __getitem__(self, item):
#         return self.q[item]
#
#     def has_next(self):
#         return len(self.q) > 0
#
#     def push(self, task_id):
#         with self.lock:
#             self.q.append(task_id)
#
#     def pop(self):
#         with self.lock:
#             if len(self.q) > 0:
#                 return self.q.pop(0)
#             else:
#                 return None
#
#     def size(self):
#         return len(self.q)
#
#     def clear(self):
#         with self.lock:
#             self.q.clear()

class TaskQueue:

    def __init__(self):
        # self.lock = threading.RLock()
        self.q = []

    # def __getitem__(self, item):
    #     return self.q[item]

    def list(self):
        ids = TaskQueueDB.objects.all().order_by('id').values_list('task_id', flat=True)
        return list(ids)

    def push(self, task_id):
        task = TaskQueueDB()
        task.task_id = task_id
        task.save()

    def pop(self):
        min_id = TaskQueueDB.objects.all().order_by('id').first().task_id
        if min_id:
            TaskQueueDB.objects.filter(task_id=min_id).delete()
        # result = TaskQueueDB.objects.filter(id=min_id)
        # if min_id is not None:
        #     return min_id
        # else:
        return min_id

    def size(self):
        return TaskQueueDB.objects.all().count()

    def clear(self):
        TaskQueueDB.objects.all().delete()


# if __name__ == '__main__':
    # min_id = TaskQueueDB.objects.all().order_by('id').first().id