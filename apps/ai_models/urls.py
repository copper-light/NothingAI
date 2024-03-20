from django.urls import re_path
from rest_framework import routers
from .views import ModelViewSet, ModelFilesViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'models/(?P<id>\d+)/files(?P<path>.*)', ModelFilesViewSet, basename='files')
router.register(r'models', ModelViewSet, basename='models')

urlpatterns = router.urls
