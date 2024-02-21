from django.shortcuts import render
from rest_framework import viewsets

from apps.experiments.models import Experiment
from apps.experiments.serializers import ExperimentSerializer


# Create your views here.
class ExperimentViewSet(viewsets.ModelViewSet):
    # renderer_classes = (CommonRenderer,)
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
