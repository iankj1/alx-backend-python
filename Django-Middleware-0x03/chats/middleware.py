import logging
from datetime import datetime, timedelta
from django.http import JsonResponse

# Store request counts: { ip_address: [datetime1, datetime2, ...] }
request_counts = {}

# ---------------------------------------------
# Middleware 1: Logs all user requests
# ---------------------------------------------
class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        logging.basicConfig(
            filename='requests.log',
            level=logging.INFO,
            format='%(message)s'
        )

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_message)
        return self.get_response(request)

# ---------------------------------------------
# Middleware 2: Limits messages per IP per minute
# ---------------------------------------------
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "POST":
            ip = self.get_client_ip(request)
            now = datetime.now()

            # Clean up timestamps older than 1 minute
            timestamps = request_counts.get(ip, [])
            timestamps = [ts for ts in timestamps if now - ts < timedelta(minutes=1)]

            # Add current request timestamp
            timestamps.append(now)
            request_counts[ip] = timestamps

            # Block if limit exceeded
            if len(timestamps) > 5:
                return JsonResponse(
                    {"error": "Too many messages. Please wait a minute."},
                    status=429
                )

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
