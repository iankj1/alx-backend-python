@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.id:
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
