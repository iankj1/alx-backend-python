
# messaging_app/chats/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Conversation, Message

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp']

# Conversation Serializer with nested messages
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'messages']
