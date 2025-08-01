from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

# 1. Automatically create notification when new message is created
@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)


# 2. Log old message content when message is edited
@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.id:  # Check if this is an update
        try:
            original = Message.objects.get(pk=instance.id)
            if original.content != instance.content:
                MessageHistory.objects.create(
                    message=original,
                    old_content=original.content,
                    edited_by=getattr(instance, '_edited_by_user', None)
                )
                instance.edited = True
        except Message.DoesNotExist:
            pass


# 3. Clean up user-related data after account deletion
@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    # 1. Delete messages sent or received
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # 2. Delete notifications
    Notification.objects.filter(user=instance).delete()

    # 3. Delete edit histories edited by the user
    MessageHistory.objects.filter(edited_by=instance).delete()
