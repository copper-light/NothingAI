import subprocess
import sys
import os
import psutil
from abc import abstractmethod
import multiprocessing

import common.code
import config.settings
from apps.experiments.models import Experiment
from common import utils
from config import settings
from common.utils import copy_files, TaskLogger
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
        self.task.status = str(C.TASK_STATUS.DONE)
        self.task.save()
        return True

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

    def _create_venv(self, working_dir, venv_name, python_version, task_logger: TaskLogger):
        with subprocess.Popen(
                [f"cd {working_dir} &&  virtualenv {venv_name} -p  {python_version}"],
                shell=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
        ) as process:
            while process.stdout.readable():
                line = process.stdout.readline()
                if not line:
                    break
                task_logger.write(line)

        process.wait()
        return process.returncode == 0

    def _install_library(self, working_dir, venv_name, task_logger: TaskLogger):
        with subprocess.Popen(
                [f"cd {working_dir} && source {venv_name}/bin/activate && pip install -r requirements.txt"],
                shell=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
        ) as process:
            while process.stdout.readable():
                line = process.stdout.readline()
                if not line:
                    break
                task_logger.write(line)

        process.wait()
        return process.returncode == 0

    def load_task(self, task_id: int) -> bool:
        self.task = Task.objects.get(pk=task_id)
        # self.task_path = None
        return self.task is not None

    def prepare_env(self) -> bool:
        task = self.task
        task_id = task.id
        exp_id = task.experiment_id
        model_id = task.experiment.model_id
        python_version = task.experiment.model.envs_info
        dataset_id = task.experiment.dataset_id

        task.status = str(C.TASK_STATUS.PREPARE)
        task.host = 'localhost'
        task.save()

        task_out_dir = settings.TASKS_LOG_DIR.format(str(task.id))
        task_logger = TaskLogger(task_out_dir)

        # 파일 복사
        try:
            # Copy Model
            task_logger.write("Copy the Model code ===")
            src = os.path.join(settings.MODELS_DIR, str(model_id))
            dst = os.path.join(settings.EXPERIMENTS_DIR, str(exp_id), str(task_id))
            copy_files(src, dst, overwrite=True)
        except FileNotFoundError as e:
            logger.info(e)
            task_logger.write(str(e))
            task_logger.write("error: model files not found")
            task.status = str(C.TASK_STATUS.FAILED)
            task.save()
            return False

        try:
            # Copy Dataset
            task_logger.write('')
            task_logger.write('')
            task_logger.write("Copy the Dataset ===")
            src = os.path.join(settings.DATASETS_DIR, str(dataset_id))
            dst = os.path.join(settings.EXPERIMENTS_DIR, str(exp_id), str(task_id))
            copy_files(src, dst, overwrite=True)
        except FileNotFoundError as e:
            logger.info(e)
            task_logger.write(str(e))
            task_logger.write("error: dataset files not found")
            task.status = str(C.TASK_STATUS.FAILED)
            task.save()
            return False

        logger.info(f"Prepare local venv : working dir {task_out_dir}")
        task_logger.write('')
        task_logger.write('')
        task_logger.write("create virtual env ===")
        python_version = C.PYTHON_VERSION()[python_version].name
        result = self._create_venv(dst, 'venv', python_version, task_logger)

        if not result:
            task_logger.write("error: fail to create virtual env")
            task.status = str(C.TASK_STATUS.FAILED)
            task.save()
            return False

        task_logger.write('')
        task_logger.write('')
        task_logger.write("Install python library ===")
        result = self._install_library(dst, 'venv', task_logger)
        if not result:
            task_logger.write("error: fail to install python library")
            task.status = str(C.TASK_STATUS.FAILED)
            task.save()
            return False

        return True

    def exec_task(self, root_dir=settings.EXPERIMENTS_DIR, *args) -> bool:
        task = self.task
        exp_id = task.experiment_id
        run_file = task.experiment.model.run_file_path

        working_dir = os.path.join(root_dir, str(exp_id), str(task.id))
        if not os.path.exists(os.path.join(working_dir, run_file)):
            logger.info("Not found run file {}".format(run_file))
            return False

        logger.info('start task {}'.format(task.id))

        process = subprocess.Popen(
            ["python3", run_file], cwd=working_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
        )

        task.status = str(C.TASK_STATUS.RUNNING)
        task.process_id = process.pid
        task.save()

        task_out_dir = settings.TASKS_LOG_DIR.format(str(task.id))
        task_logger = TaskLogger(task_out_dir, clear_logs=False)

        task_logger.write('')
        task_logger.write('')
        task_logger.write("Exec the python task ===")
        while process.poll() is None:
            line = process.stdout.readline()
            if not line:
                break
            task_logger.write(line)

        process.wait()
        return True

    def post_task(self, result: bool, *args) -> bool:
        result_type = self.task.experiment.model.result_type
        result_uri = self.task.experiment.model.result_uri
        task_out_dir = settings.TASKS_LOG_DIR.format(str(self.task.id))
        task_logger = TaskLogger(task_out_dir, clear_logs=False)
        exp_id = self.task.experiment_id
        task_id = self.task.id

        if result_type == common.code.STORAGE_TYPE.LOCAL:
            task_logger.write("Copy the Result ===")
            if result_uri is not None:
                if result_uri.startswith("/"):
                    result_uri = result_uri[1:]
                src = os.path.join(settings.EXPERIMENTS_DIR, str(exp_id), str(task_id), result_uri)
                if os.path.exists(src):
                    dst = settings.TASKS_RESULT_DIR.format(str(task_id))
                    if not os.path.exists(dst):
                        os.makedirs(dst)
                    copy_files(src, dst, overwrite=True)
                else:
                    task_logger.write('Not found result: {}'.format(result_uri))

        task_logger.write('')
        task_logger.write('')

        if result:
            task_logger.write('Finished the task ===')

            self.task.status = str(C.TASK_STATUS.DONE)
            self.task.save()
            logger.info('Finished task {}'.format(task_id))
        else:
            task_logger.write('Fail the task ===')
            self.task.status = str(C.TASK_STATUS.FAILED)
            self.task.save()
            logger.info('Fail the task: {}'.format(task_id))

        return result

    def is_suspend(self) -> bool:
        task = self.task
        if (task.status == C.TASK_STATUS.DONE) or (task.status == C.TASK_STATUS.FAILED):
            return False

        ret = False
        if not self.is_running():
            task_output_file = os.path.join(settings.TASKS_LOG_DIR.format(str(task.id)), settings.TASKS_LOG_FILENAME)
            if os.path.exists(task_output_file):
                line = tailer.tail(open(task_output_file), 1)
                if line is not None:
                    if line[0].find(':Finished the task ===') == -1:
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
            if str(process.pid) == pid:
                ret = True
                break

        return ret
