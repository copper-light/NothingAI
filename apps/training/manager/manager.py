import os
from threading import Thread
import multiprocessing
from multiprocessing import Process
from apscheduler.schedulers.background import BackgroundScheduler
from django.shortcuts import get_object_or_404

from apps.experiments.models import Experiment
from apps.training.manager.task_queue import TaskQueue
from apps.training.manager.task_pool import TaskPool
from apps.training.models import Task
import common.code as C

import logging
import psutil
import time

from apps.training.runner.runner import LocalRunner, Runner

logger = logging.getLogger(__name__)


multiprocessing.set_start_method('spawn')


# def work(queue: TaskQueue, pool: TaskPool):
#     while True:
#         if queue.size() > 0:
#             if pool.empty_size() > 0:
#                 value = queue.pop()
#                 pool.add_task(value)
#                 logger.debug(("work", value, queue.size()))
#             else:
#                 logger.debug("not empty pool")
#                 time.sleep(5)
#         else:
#             logger.debug(f"Empty task queue {queue.size()}")
#             time.sleep(10)

def work():
    logger.info("working scheduler")

    mgr = TrainingManager.getinstance()

    queue = mgr.task_queue
    pool = mgr.task_pool

    # 작업이 완료된 task를 pool에서 제거하는 로직에 대한 개선 필요
    if pool.size() > 0:
        ids = pool.list()
        for task_id in ids:
            runner = LocalRunner(task_id)
            suspend = runner.is_suspend()
            if suspend:
                mgr.run_task(task_id, run_last_step=True)
            else:
                if not runner.is_running():
                    pool.remove_task(task_id)

    for _ in queue.list():
        if pool.empty_size() > 0:
            task_id = queue.pop()
            pool.add_task(task_id)
            logger.debug(("running new task", task_id, pool.size()))

            # task = Task.objects.get(pk=task_id)
            runner = LocalRunner(task_id)
            mgr.run_task(task_id, run_last_step=True)
            # source_type = task.experiment.model.source_type

            # if source_type == c.STORAGE_TYPE.LOCAL:
            #     runner = LocalRunner()
            # else:
            #     runner = ...

        else:
            break

    logger.debug(f"queue info (size {queue.size()}) : {queue.list()}")
    logger.debug(f"pool info (size {pool.size()}/{pool.limit}) : {pool.list()}")

    # if pool.size() > 0:
    #     ids = pool.list()
    #     # logger.debug(f"remove work {ids[0]}")
    #     pool.remove_task(ids[0])


def process_task(task_id, run_last_step):
    runner = LocalRunner(task_id)
    runner.prepare_env()
    result = runner.exec_task()
    runner.post_task(result)
    # runner.clear()


class TrainingManager:
    _instance = None
    _monitor_thread = None
    SCHEDULER_ID = 'TaskQueueMonitor'
    init_check = False

    @classmethod
    def getinstance(cls):
        # logger.info(f"load {cls._instance} {os.getpid()}")
        if cls._instance is None:
            cls._instance = TrainingManager()
        return cls._instance

    def __init__(self):
        self.task_queue = TaskQueue()
        self.task_pool = TaskPool(limit=3)

        scheduler = BackgroundScheduler()
        scheduler.add_job(work, 'interval', seconds=10, id=self.SCHEDULER_ID)
        self._scheduler = scheduler

    def add_experiment(self, experiment_id):
        # 실행 계획 생성
        get_object_or_404(Experiment, pk=experiment_id)

        task = Task()
        task.experiment_id = experiment_id
        task.save()
        # queue에 삽입
        logger.info(f"Task pushed to the queue: Task ID {task.id}", )
        self.task_queue.push(task.id)

    def start(self):
        # if self._monitor_thread is not None and self._monitor_thread.is_alive():
        #     logger.info('TrainingManager is already running')
        #     return False
        #
        # self._monitor_thread = Thread(target=work, args=(self.task_queue, self.task_pool, ))
        # self._monitor_thread.start()
        #
        # scheduler = BackgroundScheduler()
        # scheduler.add_job(work, 'interval', seconds=30, id='TaskQueueMonitor')
        # scheduler.start()

        # 기존 준비된 테스크를 실행하고 점검
        if self._scheduler.running:
            logger.info('TrainingManager is already running')
        else:
            self._scheduler.start()
            logger.info('Start TrainingManager')
        return True

    def stop(self):
        # if self._monitor_thread is not None:
        #     self._monitor_thread.join()
        #     self._monitor_thread = None
        if self._scheduler.running:
            self._scheduler.shutdown()
        else:
            logger.info('TrainingManager is not running')

    def run_task(self, task_id, run_last_step=False):
        Process(target=process_task, args=(task_id, run_last_step,)).start()


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
