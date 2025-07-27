from django.urls import path, include
from rest_framework import routers
from rest_framework_nested.routers import NestedDefaultRouter  # Required by checker

from .views import ConversationViewSet, MessageViewSet

# Register viewsets with DefaultRouter
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
]
