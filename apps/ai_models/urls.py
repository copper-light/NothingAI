from rest_framework import routers
from .views import ModelViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'models', ModelViewSet, basename='models')

urlpatterns = router.urls
