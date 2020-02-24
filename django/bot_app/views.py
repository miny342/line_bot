from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

# Create your views here.
class CallbackView(View):
    def post(self, request, *args, **kwargs):
        return HttpResponse()