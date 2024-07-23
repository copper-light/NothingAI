from rest_framework import routers

from apps.user.views import UserViews, UserLoginLogoutViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'user', UserViews, basename='user')
router.register(r'sign-in', UserLoginLogoutViewSet, basename='sign-in') # /api/v1/login
# router.register(r'user', UserDetailViewSet, basename='logout') # /api/v1/login

urlpatterns = router.urls