from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to:
    - Allow only authenticated users
    - Allow only participants in a conversation to view, send, update or delete messages
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # If object is a Message
        if hasattr(obj, 'sender'):
            return (
                obj.sender == request.user or
                request.user in obj.conversation.participants.all()
            )

        # If object is a Conversation
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()

        return False
