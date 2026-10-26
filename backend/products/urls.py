from rest_framework import routers
from . import api

urlpatterns = []

router = routers.DefaultRouter()
router.register("", api.ProductViewSet)
urlpatterns += router.urls
