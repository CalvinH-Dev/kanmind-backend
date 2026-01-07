from django.urls import path
from rest_framework import routers

from tasks_app.api.views import AssignedToMeView, ReviewingView, TaskViewSet

urlpatterns = [
    path("assigned-to-me/", AssignedToMeView.as_view()),
    path("reviewing/", ReviewingView.as_view()),
]

router = routers.SimpleRouter()
router.register(r"", TaskViewSet, basename="tasks")

urlpatterns += router.urls
