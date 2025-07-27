import os
from datetime import datetime, time
import logging
from django.http import HttpResponseForbidden

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

log_path = os.path.join(BASE_DIR, 'requests.log')

logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        logging.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        return self.get_response(request)


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()
        start_time = time(18, 0)  # 6:00 PM
        end_time = time(21, 0)    # 9:00 PM

        # Only restrict for chat-related paths
        if request.path.startswith('/chats/'):
            if not (start_time <= now <= end_time):
                return HttpResponseForbidden("Access to chats is restricted to between 6PM and 9PM.")

        return self.get_response(request)
