import subprocess
import sys
import os
from config import settings


def exec_experiment(run_file: str, experiment_dir: str, root_dir=settings.FILE_UPLOAD_DIR) -> bool:
    if experiment_dir is not None and experiment_dir.startswith('/'):
        experiment_dir = experiment_dir[1:]
    working_dir = os.path.join(root_dir, experiment_dir)
    # session = subprocess.run(["python3", run_file], cwd=working_dir, stdout=subprocess.PIPE)
    # print(session)

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
