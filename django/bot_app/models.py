from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.
class LineUser(models.model):
    userid = models.CharField(max_length=128, primary=True)
    data = JSONField(default={})

class ChatHistory(models.Model):
    user = models.ForeignKey(LineUser, on_delete=models.CASCADE, related_name="chat")
    chat = JSONField()
