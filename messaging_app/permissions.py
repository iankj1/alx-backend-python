from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsParticipantOfConversation(BasePermission):
    """
    Allows access only to participants of a conversation.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        if not user.is_authenticated:
            return False

        # If the object is a conversation
        if hasattr(obj, 'participants'):
            return user in obj.participants.all()

        # If the object is a message, check if user is part of the message's conversation
        if hasattr(obj, 'conversation'):
            return user in obj.conversation.participants.all()

        return False
