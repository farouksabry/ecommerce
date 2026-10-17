from rest_framework import routers
from .api import OrderViewSet, OrderItemViewSet

urlpatterns = []

router = routers.DefaultRouter()
router.register("orders", OrderViewSet)
router.register("orderitems", OrderItemViewSet)
urlpatterns += router.urls
