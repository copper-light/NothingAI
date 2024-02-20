from rest_framework import routers
from .views import AIModelViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register('models', AIModelViewSet)

urlpatterns = router.urls
