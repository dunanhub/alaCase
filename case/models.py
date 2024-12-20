from django.contrib.auth.models import User
from django.db import models


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return f"{self.user_id}: {self.username}"

