import os
import logging
from datetime import datetime
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.log_file = os.path.join(os.path.dirname(__file__), '../requests.log')
        logging.basicConfig(filename=self.log_file, level=logging.INFO)

    def __call__(self, request):
        logging.info(f"{datetime.now()} - {request.method} request to {request.path}")
        return self.get_response(request)


class OffensiveLanguageMiddleware:
    offensive_words = ['damn', 'hell', 'shit', 'fuck']

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            body_content = request.body.decode('utf-8')
            for word in self.offensive_words:
                if word in body_content.lower():
                    return HttpResponseForbidden("Offensive language detected.")
        except Exception:
            pass  # Allow if body can't be decoded
        return self.get_response(request)


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        if current_hour < 18 or current_hour >= 21:
            return HttpResponseForbidden("Chat access is only allowed between 6PM and 9PM.")
        return self.get_response(request)


class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            role = getattr(user, 'role', 'user')
            if role not in ['admin', 'moderator']:
                return HttpResponseForbidden("You do not have permission to perform this action.")
        return self.get_response(request)
