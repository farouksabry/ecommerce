from rest_framework import routers
from . import api

urlpatterns = [
]

router = routers.DefaultRouter()
router.register("", api.UserViewSet)
urlpatterns += router.urls
