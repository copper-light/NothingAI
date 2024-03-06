from rest_framework import routers
from .views import DatasetViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'datasets', DatasetViewSet, basename='datasets')

urlpatterns = router.urls
