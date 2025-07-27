from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation to access or modify it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # Read permissions (GET, HEAD, OPTIONS)
            if hasattr(obj, 'sender'):
                return request.user in obj.conversation.participants.all()
            if hasattr(obj, 'participants'):
                return request.user in obj.participants.all()
        elif request.method in ['PUT', 'PATCH', 'DELETE']:
            # Write permissions
            if hasattr(obj, 'sender'):
                return obj.sender == request.user
            if hasattr(obj, 'participants'):
                return request.user in obj.participants.all()
        return False
