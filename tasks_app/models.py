from django.db import models

from auth_app.models import UserProfile
from boards_app.models import Board

# Create your models here.


class Task(models.Model):
    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"

    class Status(models.TextChoices):
        REVIEW = "review", "Review"
        DONE = "done", "Done"
        TODO = "to-do", "To Do"
        IN_PROGRESS = "in-progress", "In Progress"

    creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
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
        max_length=6, choices=Priority.choices, default=Priority.MEDIUM
    )

    status = models.CharField(
        max_length=11, choices=Status.choices, default=Status.TODO
    )
    due_date = models.DateField()

    def __str__(self):
        return self.title


class Comment(models.Model):
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
