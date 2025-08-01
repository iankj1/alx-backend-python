from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message
from django.db.models import Prefetch

@login_required
def threaded_messages_view(request):
    # Filter top-level messages involving current user
    top_messages = Message.objects.filter(
        parent_message__isnull=True
    ).filter(
        sender=request.user
    ).select_related('sender', 'receiver') \
     .prefetch_related(
         Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver').order_by('timestamp'))
     ).order_by('-timestamp')

    context = {
        'messages': top_messages
    }
    return render(request, 'messaging/threaded_messages.html', context)

# ✅ NEW: For unread messages using the custom manager
@login_required
def unread_messages_view(request):
    unread_msgs = Message.unread.unread_for_user(request.user)
    return render(request, 'messaging/unread_messages.html', {
        'unread_messages': unread_msgs
    })
