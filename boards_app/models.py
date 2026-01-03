from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Board(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="board_owner"
    )
    members = models.ManyToManyField(User, related_name="board_members")
    title = models.CharField(max_length=254)

    def __str__(self):
        return self.title
