import os

from django.apps import AppConfig


class TrainingConfig(AppConfig):
    name = 'apps.training'

    def ready(self):
        print("os.environ.get('LoadedTrainingConfig')", os.environ.get('LoadedTrainingConfig'))
        if not os.environ.get('LoadedTrainingConfig'):
            os.environ['LoadedTrainingConfig'] = 'True'
            from apps.training.manager.manager import TrainingManager
            manager = TrainingManager.getinstance()
            manager.start()
        else:
            os.environ['LoadedTrainingConfig'] = 'False'
            print("asdfa")
