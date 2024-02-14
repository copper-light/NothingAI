from rest_framework import routers
from .views import AIModelViewSet

router = routers.SimpleRouter()
router.register('', AIModelViewSet)

urlpatterns = router.urls
