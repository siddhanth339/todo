from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Task(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="tasks") 
    description = models.TextField(max_length = 50)