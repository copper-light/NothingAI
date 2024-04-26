import subprocess
import sys
import os
import psutil
from abc import abstractmethod
import multiprocessing

import config.settings
from apps.experiments.models import Experiment
from config import settings
from common.utils import copy_files
import common.code as C

from apps.training.models import Task

import tailer
import logging

logger = logging.getLogger(__name__)


class Runner(object):

    def __init__(self, task_id: int = None):
        self.task = None
        if not self.load_task(task_id):
            raise Exception("Not loaded task {}".format(task_id))

    def load_task(self, task_id: int) -> bool:
        self.task = Task.objects.get(pk=task_id)
        return self.task is not None

    @abstractmethod
    def prepare_env(self, *args) -> bool:
        pass

    @abstractmethod
    def exec_task(self, *args) -> bool:
        pass

    def post_task(self, *args) -> bool:
        pass

    def clear(self) -> bool:
        if self.task:
            task = Task.objects.get(id=self.task.id)
            if task:
                task.delete()
                self.task = None
                return True
            else:
                raise Exception("Not found task {}".format(task.id))
        else:
            return False


class LocalRunner(Runner):

    def load_task(self, task_id: int) -> bool:
        self.task = Task.objects.get(pk=task_id)
        self.task_path = None
        return self.task is not None

    def prepare_env(self) -> bool:
        task = self.task
        task_id = task.id
        exp_id = task.experiment_id
        model_id = task.experiment.model_id
        # dataset_id = task.dataset_id

        task.status = str(C.TASK_STATUS.PREPARE)
        task.host = 'localhost'
        task.save()

        # 파일 복사
        src = os.path.join(settings.MODELS_DIR, str(model_id))
        dst = os.path.join(settings.EXPERIMENTS_DIR, str(exp_id), str(task_id))
        copy_files(src, dst, overwrite=True)

        # 가상환경 구성

        # 라이브러리 다운로드

        return True

    def exec_task(self, root_dir=settings.EXPERIMENTS_DIR, *args) -> bool:
        task = self.task
        exp_id = task.experiment_id
        run_file = task.experiment.model.run_file_path

        working_dir = os.path.join(root_dir, str(exp_id), str(task.id))
        if not os.path.exists(os.path.join(working_dir, run_file)):
            logger.info("Not found run file {}".format(run_file))
            return False

        task_out_dir = os.path.join(settings.TASKS_LOG_DIR, str(task.id))
        if not os.path.exists(task_out_dir):
            os.makedirs(task_out_dir)

        logger.info('start task {}'.format(task.id))

        f = open(os.path.join(task_out_dir, config.settings.TASKS_LOG_FILENAME), 'w')
        # process = subprocess.Popen(
        #     ["python3", run_file], cwd=working_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        # )

        process = subprocess.Popen(
            ["python3", run_file], cwd=working_dir, stdout=f, stderr=f
        )
        process.wait()
        f.write('\n\nFinished: Success')
        f.close()

        task.status = str(C.TASK_STATUS.RUNNING)
        task.process_id = process.pid
        task.save()

        # while process.poll() is None:
        #     line = process.stdout.readline()
        #     if not line:
        #         break
        #     f.write(str(line, 'utf8'))
        # f.write('\n\nFinished: Success')

        logger.info('Finished task {}'.format(task.id))
        return True

    def is_suspend(self) -> bool:
        task = self.task
        if (task.status == C.TASK_STATUS.DONE) or (task.status == C.TASK_STATUS.FAILED):
            return False

        ret = False
        if not self.is_running():
            task_output_file = os.path.join(settings.TASKS_LOG_DIR, str(task.id), settings.TASKS_LOG_FILENAME)
            if os.path.exists(task_output_file):
                line = tailer.tail(open(task_output_file), 1)
                if line is not None:
                    if line[0].find('Finished:') == -1:
                        ret = True
                else:
                    ret = True
            else:
                ret = True

        return ret

    def is_running(self) -> bool:
        task = self.task
        pid = task.process_id
        ret = False
        for process in psutil.process_iter():
            if process.pid == pid:
                ret = True
                break

        return ret
