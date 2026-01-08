from django.urls import path
from rest_framework import routers

from tasks_app.api.views import (
    AssignedToMeView,
    CommentsViewSet,
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
        CommentsViewSet.as_view({"get": "list", "post": "create"}),
        name="task-comments",
    ),
    # path(
    #     "<int:task_id>/comments/<int:pk>/",
    #     CommentViewSet.as_view(
    #         {
    #             "get": "retrieve",
    #             "put": "update",
    #             "patch": "partial_update",
    #             "delete": "destroy",
    #         }
    #     ),
    #     name="task-comment-detail",
    # ),
]

urlpatterns += router.urls
urlpatterns += comment_urls
