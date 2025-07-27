from rest_framework import permissions

class IsOwnerOrParticipant(permissions.BasePermission):
    """
    Custom permission to allow only conversation participants to view messages.
    """

    def has_object_permission(self, request, view, obj):
        # For messages
        if hasattr(obj, 'sender'):
            return obj.sender == request.user or request.user in obj.conversation.participants.all()
        # For conversations
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        return False
