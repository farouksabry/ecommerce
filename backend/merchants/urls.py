from rest_framework import routers
from .api import MerchantViewSet, StoreViewSet

urlpatterns = []

router = routers.DefaultRouter()
router.register("merchants", MerchantViewSet)
router.register("stores", StoreViewSet)
urlpatterns += router.urls
