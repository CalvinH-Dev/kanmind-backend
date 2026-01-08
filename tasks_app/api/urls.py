from django.urls import path
from rest_framework import routers

from tasks_app.api.views import (
    AssignedToMeView,
    CommentDeleteAPI,
    CommentsListCreateAPI,
    ReviewingView,
    TaskViewSet,
)

urlpatterns = [
    path("assigned-to-me/", AssignedToMeView.as_view()),
    path("reviewing/", ReviewingView.as_view()),
]

router = routers.SimpleRouter()
router.register(r"", TaskViewSet, basename="tasks")


comment_urls = [
    path(
        "<int:task_id>/comments/",
        CommentsListCreateAPI.as_view(),
        name="task-comments",
    ),
    path(
        "<int:task_id>/comments/<int:pk>/",
        CommentDeleteAPI.as_view(),
        name="task-comment-detail",
    ),
]

urlpatterns += router.urls
urlpatterns += comment_urls
