from django.db import models

from auth_app.models import UserProfile


class Board(models.Model):
    """
    Model representing a board with an owner and multiple members.

    A Board is owned by a single UserProfile and can have multiple
    UserProfile members associated with it. Boards also have a title
    to identify them.
    """

    owner = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="board_owner",
    )
    members = models.ManyToManyField(
        UserProfile,
        related_name="board_members",
    )
    title = models.CharField(max_length=254)

    def __str__(self):
        return self.title
