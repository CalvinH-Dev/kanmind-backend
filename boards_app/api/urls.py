from rest_framework import routers

from boards_app.api.views import BoardsViewSet

router = routers.SimpleRouter()
router.register(r"", BoardsViewSet, basename="boards")

urlpatterns = router.urls
