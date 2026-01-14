from django.db import models

from auth_app.models import UserProfile
from boards_app.models import Board


class Task(models.Model):
    """
    Model representing a task within a board.

    A Task is linked to a board and a creator profile. It can
    optionally have an assignee and a reviewer. Priority and
    status fields are limited to predefined text choices, and
    each task has a due date.
    """

    class Priority(models.TextChoices):
        """
        Predefined priority options for a task.

        LOW: low priority task.
        MEDIUM: normal priority task (default).
        HIGH: high priority task.
        """

        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"

    class Status(models.TextChoices):
        """
        Predefined status options for a task.

        REVIEW: task under review.
        DONE: completed task.
        TODO: not started yet (default).
        IN_PROGRESS: currently being worked on.
        """

        REVIEW = "review", "Review"
        DONE = "done", "Done"
        TODO = "to-do", "To Do"
        IN_PROGRESS = "in-progress", "In Progress"

    creator = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
    )
    board = models.ForeignKey(
        Board, on_delete=models.CASCADE, related_name="tickets"
    )
    title = models.CharField(max_length=254)
    description = models.TextField(blank=True)
    assignee = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        related_name="tasks_assigned",
    )
    reviewer = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        related_name="tasks_reviewing",
    )
    priority = models.CharField(
        max_length=6,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )
    status = models.CharField(
        max_length=11,
        choices=Status.choices,
        default=Status.TODO,
    )
    due_date = models.DateField()

    def __str__(self):
        return f"Board: {self.board.title} - Task: {self.title}"


class Comment(models.Model):
    """
    Model representing a comment on a task.

    Each comment is linked to a specific Task and an author
    UserProfile. The content is optional (empty string allowed),
    and creation time is automatically recorded.
    """

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"Author: {self.author} - "
            f"Comment: {self.content} - "
            f"Created at: {self.created_at.strftime('%a, %d.%m.%Y %H:%M')}"
        )
