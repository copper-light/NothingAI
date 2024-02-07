from queue import Queue


class Scheduler:

    def __init__(self):
        self._queue = Queue()
        self._urgent_queue = Queue()

    def get_worker_len(self):
        return self._queue.qsize() + self._urgent_queue.qsize()

    def put(self, work, urgent=False):
        if urgent:
            self._urgent_queue.put(work)
        else:
            self._queue.put(work)

