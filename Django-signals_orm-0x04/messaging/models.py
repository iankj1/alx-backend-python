from django.db import models
from django.contrib.auth.models import User
from .managers import UnreadMessagesManager

class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        return self.get_queryset().filter(
            receiver=user,
            read=False
        ).select_related('sender').only('sender', 'content', 'timestamp')

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
     parent_message = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    read = models.BooleanField(default=False)

    objects = models.Manager()  # default manager
    unread = UnreadMessagesManager()  # custom manager for unread messages

def __str__(self):
        return f'From {self.sender} to {self.receiver}: {self.content[:20]}'
    
    # 🔁 Threaded replies (self-referential FK)
    parent_message = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )

    def __str__(self):
        return f"From {self.sender} to {self.receiver} at {self.timestamp}"

    def get_thread(self):
        thread = []
        for reply in self.replies.all().order_by('timestamp'):
            thread.append(reply)
            thread.extend(reply.get_thread())
        return thread

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user} about message {self.message.id}"


class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='edit_logs')

    def __str__(self):
        return f"Edit history of message {self.message.id} at {self.edited_at}"
