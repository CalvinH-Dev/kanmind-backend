from rest_framework import routers

from tasks_app.api.views import TaskViewSet

router = routers.SimpleRouter()
router.register(r"", TaskViewSet, basename="tasks")

urlpatterns = router.urls
