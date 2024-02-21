from rest_framework import routers
from .views import ExperimentViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register('experiments', ExperimentViewSet)

urlpatterns = router.urls
