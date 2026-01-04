from django.contrib.auth.models import User
from django.db import models

from auth_app.models import UserProfile

# Create your models here.


class Board(models.Model):
    owner = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="board_owner"
    )
    members = models.ManyToManyField(UserProfile, related_name="board_members")
    title = models.CharField(max_length=254)

    def __str__(self):
        return self.title
