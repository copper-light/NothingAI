from common.routers import FileRouter
from .views import DatasetViewSet

router = FileRouter(trailing_slash=False)
router.register(r'datasets', DatasetViewSet, basename='datasets')

urlpatterns = router.urls
