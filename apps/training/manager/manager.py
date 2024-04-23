import os
from threading import Thread

# from multiprocessing import Process

from apps.training.manager.task_queue import TaskQueue
from apps.training.manager.task_pool import TaskPool

from apps.training.models import Task

import logging
import time

logger = logging.getLogger(__name__)


def work(queue: TaskQueue, pool: TaskPool):
    while True:
        if queue.size() > 0:
            if pool.empty_size() > 0:
                value = queue.pop()
                pool.add_task(value)
                logger.debug(("work", value, queue.size()))
            else:
                logger.debug("not empty pool")
                time.sleep(5)
        else:
            logger.debug(f"Empty task queue {queue.size()}")
            time.sleep(10)


class TrainingManager:
    _instance = None
    _monitor_thread = None

    @classmethod
    def getinstance(cls):
        logger.info(f"load {cls._instance} {os.getpid()}")
        if cls._instance is None:
            cls._instance = TrainingManager()
            logger.info(f"create {cls._instance}")
        return cls._instance

    def __init__(self):
        self.task_queue = TaskQueue()
        self.task_pool = TaskPool(limit=3)

    def add_experiment(self, experiment_id):
        # 실행 계획 생성
        task = Task()
        task.experiment_id = experiment_id
        task.save()
        logger.info(("task_id", task.id))
        # queue에 삽입
        self.task_queue.push(task.id)
        logger.info(self.task_queue.size())

    def start(self):
        if self._monitor_thread is not None and self._monitor_thread.is_alive():
            logger.info('TrainingManager thread is already running')
            return False

        self._monitor_thread = Thread(target=work, args=(self.task_queue, self.task_pool, ))
        self._monitor_thread.start()

        logger.info('Start TrainingManager')
        return True

    def stop(self):
        if self._monitor_thread is not None:
            self._monitor_thread.join()
            self._monitor_thread = None


if __name__ == '__main__':
    manager = TrainingManager.getinstance()

    # manager.add_experiment(20)
    # manager.add_experiment(500)
    # manager.add_experiment(10)
    # manager.add_experiment(20)
    # manager.add_experiment(500)
    # manager.add_experiment(10)
    # manager.add_experiment('asdf')
    # manager.add_experiment('zxcv')
    # manager.add_experiment('qwer')
    # manager.add_experiment('cvbn')
    # manager.add_experiment(20)
    # manager.add_experiment(500)
    # manager.add_experiment(10)
    #
    # manager.start()
    #
    # while manager.task_queue.size() > 0:
    #     if manager.task_pool.size() > 0:
    #         l = manager.task_pool.get_list()
    #         time.sleep(5)
    #
    #         manager.task_pool.remove_task(l[0])
