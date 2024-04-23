
class TaskPool(object):
    def __init__(self, limit=1):
        self.task = {}
        self.limit = limit
        self.count = 0

    def get_list(self):
        return list(self.task.keys())

    def add_task(self, task_id):
        if self.count < self.limit:
            self.task[task_id] = task_id
            self.count += 1
        else:
            raise OverflowError("TaskPool is overflowed")

    def remove_task(self, task_id):
        if task_id in self.task:
            self.task[task_id] = None
            self.count -= 1
        else:
            raise Exception("Task does not exist")

    def get_task(self, task_id):
        return self.task[task_id]

    def empty_size(self):
        return self.limit - self.count

    def size(self):
        return self.count
