from rest_framework import routers
from .views import ModelViewSet
from common.routers import FileRouter

router = FileRouter(trailing_slash=False)
router.register(r'models', ModelViewSet, basename='models')
urlpatterns = router.urls
