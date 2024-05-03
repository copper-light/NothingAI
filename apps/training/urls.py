from rest_framework import routers
from .views import TaskViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register('tasks', TaskViewSet)

urlpatterns = router.urls
