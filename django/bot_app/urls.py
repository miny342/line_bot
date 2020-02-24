from django.urls import path
from .views import CallbackView

urlpatterns = [
    path('', CallbackView.as_view()),
]