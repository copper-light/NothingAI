from django.urls import re_path
from rest_framework import routers
from .views import ModelViewSet, FilesViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'models/(?P<model_id>\d+)/files', FilesViewSet, basename='files')
router.register(r'models', ModelViewSet, basename='models')

urlpatterns = router.urls
