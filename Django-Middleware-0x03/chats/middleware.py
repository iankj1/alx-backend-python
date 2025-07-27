import os
from datetime import datetime
import logging
from django.http import JsonResponse

# Setup logging
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_DIR, 'requests.log')
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        log_message = f"{datetime.now()} - {request.method} request to {request.path}"
        logging.info(log_message)
        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        if current_hour < 18 or current_hour >= 21:
            return JsonResponse({'error': 'Chat access is restricted during this time.'}, status=403)
        return self.get_response(request)


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.offensive_words = ['badword1', 'badword2', 'offensiveword']

    def __call__(self, request):
        if request.method == 'POST':
            for word in self.offensive_words:
                if word in str(request.body.decode('utf-8')).lower():
                    return JsonResponse({'error': 'Offensive language is not allowed.'}, status=400)
        return self.get_response(request)


class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated:
            role = getattr(user, 'role', None)
            if role not in ['admin', 'moderator']:
                return JsonResponse({'error': 'Forbidden: Insufficient permissions'}, status=403)
        return self.get_response(request)
