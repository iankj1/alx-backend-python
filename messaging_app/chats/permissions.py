from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only authenticated users and participants
    of a conversation to access or modify it.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        # Allow safe methods (GET, HEAD, OPTIONS) if user is a participant
        if request.method in permissions.SAFE_METHODS:
            if hasattr(obj, 'sender'):
                return request.user in obj.conversation.participants.all()
            if hasattr(obj, 'participants'):
                return request.user in obj.participants.all()

        # Allow edit/delete only by sender or participants
        elif request.method in ['PUT', 'PATCH', 'DELETE']:
            if hasattr(obj, 'sender'):
                return obj.sender == request.user
            if hasattr(obj, 'participants'):
                return request.user in obj.participants.all()

        return False
