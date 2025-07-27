from django.shortcuts import render

# Create your views here.
# chats/views.py
from django.http import JsonResponse

def index(request):
    return JsonResponse({"message": "Messaging App API is live!"})
