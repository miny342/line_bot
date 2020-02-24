from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.

class UserIdModel(models.Model):
    userid = models.CharField(max_length=128, primary_key=True)

class ChatHistory(models.Model):
    user = models.ForeignKey(UserIdModel, on_delete=models.CASCADE)
    chat = JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
