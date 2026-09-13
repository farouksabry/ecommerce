from rest_framework import routers
from .api import OrderViewSet

urlpatterns = []

router = routers.DefaultRouter()
router.register("", OrderViewSet)
urlpatterns += router.urls
