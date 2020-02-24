from django.contrib import admin
from .models import UserIdModel, ChatHistory

# Register your models here.
admin.site.register(UserIdModel)
admin.site.register(ChatHistory)
