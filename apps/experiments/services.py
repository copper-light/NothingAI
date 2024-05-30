import subprocess
import os
from abc import abstractmethod

from apps.experiments.models import Experiment
from config import settings
from common.utils import copy_files


class ExecService:

    @abstractmethod
    def prepare_env(self):
        pass

    @abstractmethod
    def exec_experiment(self, experiment_name):
        pass


def prepare_experiment_env(model_id: int, dataset_id: int, exp_id: int) -> bool:
    # 파일 복사
    src = os.path.join(settings.MODELS_DIR, str(model_id))
    dst = os.path.join(settings.EXPERIMENTS_DIR, str(exp_id))
    copy_files(src, dst, overwrite=True)

    # 가상환경 구성

    # 라이브러리 다운로드

    return True


def exec_experiment(experiment: Experiment, root_dir=settings.EXPERIMENTS_DIR) -> bool:
    working_dir = os.path.join(root_dir, str(experiment.id))
    run_file = experiment.model.run_file_path
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
