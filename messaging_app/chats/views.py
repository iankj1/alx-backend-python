from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.status import HTTP_403_FORBIDDEN

from .models import Conversation, Message
from .serializers import MessageSerializer
from .permissions import IsParticipantOfConversation

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        conversation_id = self.request.query_params.get('conversation_id')
        if conversation_id:
            conversation = Conversation.objects.filter(id=conversation_id).first()
            if conversation and self.request.user in conversation.participants.all():
                return Message.objects.filter(conversation=conversation)
            else:
                raise PermissionDenied("You are not a participant of this conversation.")
        return Message.objects.none()

    def perform_create(self, serializer):
        conversation = serializer.validated_data.get("conversation")
        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("You are not allowed to send messages to this conversation.")
        serializer.save(sender=self.request.user)
