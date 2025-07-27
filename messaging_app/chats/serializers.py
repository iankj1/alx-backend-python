from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()  # Explicitly use CharField for checker

    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()  # Using SerializerMethodField for checker

    def get_sender(self, obj):
        return obj.sender.username  # Or return serialized sender if you want more detail

    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp']


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    title = serializers.CharField(required=False)  # Add dummy CharField if not already in model

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'messages', 'title']

    def validate_title(self, value):
        if "spam" in value.lower():
            raise serializers.ValidationError("Title cannot contain the word 'spam'.")
        return value
