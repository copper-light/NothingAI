import threading


class TaskQueue:

    def __init__(self):
        self.lock = threading.RLock()
        self.q = []
        # self.tasks = {}
        # self.tasks_lock = threading.Lock()
        # self.tasks_lock.acquire()
        # self.tasks_lock.release()
        # self.tasks_lock = threading.Lock()

    def __getitem__(self, item):
        return self.q[item]

    def has_next(self):
        return len(self.q) > 0

    def push(self, task_id):
        with self.lock:
            self.q.append(task_id)

    def pop(self):
        with self.lock:
            if len(self.q) > 0:
                return self.q.pop(0)
            else:
                return None

    def size(self):
        return len(self.q)

    def clear(self):
        with self.lock:
            self.q.clear()
