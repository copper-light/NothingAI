import os

from django.apps import AppConfig


class TrainingConfig(AppConfig):
    name = 'apps.training'

    def ready(self):
        if not os.environ.get('LoadedTrainingConfig'):
            os.environ['LoadedTrainingConfig'] = 'True'
            from apps.training.manager.manager import TrainingManager
            manager = TrainingManager.getinstance()
            manager.start()
