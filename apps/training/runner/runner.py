import subprocess
import sys
import os
from abc import abstractmethod

from apps.experiments.models import Experiment
from config import settings
from common.utils import copy_files

from apps.training.models import Task


class Runner(object):

    @abstractmethod
    def prepare_env(self, model_id: int, dataset_id: int, task_id: int) -> bool:
        pass

    @abstractmethod
    def exec_task(self, task_id: int, *args) -> bool:
        pass


class LocalRunner(Runner):

    def prepare_env(self, model_id: int, dataset_id: int, task_id: int) -> bool:
        # 파일 복사
        src = os.path.join(settings.MODELS_DIR, str(model_id))
        dst = os.path.join(settings.EXPERIMENTS_DIR, str(task_id))
        copy_files(src, dst, overwrite=True)

        # 가상환경 구성

        # 라이브러리 다운로드

        return True

    def exec_task(self, task_id: int, root_dir=settings.EXPERIMENTS_DIR, *args) -> bool:
        task = Task.objects.get(id=task_id)
        exp_id = task.experiment.id
        run_file = task.experiment.model.run_file_path

        working_dir = os.path.join(root_dir, str(exp_id), str(task.id))

        if not os.path.exists(os.path.join(working_dir, run_file)):
            return False

        process = subprocess.Popen(
            ["python3", run_file], cwd=working_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )

        while process.stdout.readable():
            line = process.stdout.readline()
            if not line:
                break
            print(str(line.strip(), 'utf8'))

        return True
