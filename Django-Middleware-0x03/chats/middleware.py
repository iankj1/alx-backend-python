import logging
from datetime import datetime, timedelta
from django.http import JsonResponse

# Store request counts for rate limiting: { ip_address: [datetime1, datetime2, ...] }
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
# Middleware 2: Restrict chat access between 6PM and 9PM only
# ---------------------------------------------
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()
        if request.path.startswith("/chat") or request.path.startswith("/messages"):
            # Allow access only between 6PM (18:00) and 9PM (21:00)
            if not (datetime.strptime("18:00", "%H:%M").time() <= now <= datetime.strptime("21:00", "%H:%M").time()):
                return JsonResponse(
                    {"error": "Chat access is allowed only between 6PM and 9PM."},
                    status=403
                )
        return self.get_response(request)

# ---------------------------------------------
# Middleware 3: Limit POST requests (chat messages) to 5 per minute per IP
# ---------------------------------------------
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "POST":
            ip = self.get_client_ip(request)
            now = datetime.now()

            # Remove timestamps older than 1 minute
            timestamps = request_counts.get(ip, [])
            timestamps = [ts for ts in timestamps if now - ts < timedelta(minutes=1)]

            # Append current timestamp
            timestamps.append(now)
            request_counts[ip] = timestamps

            # Check if limit exceeded
            if len(timestamps) > 5:
                return JsonResponse(
                    {"error": "Too many messages. Please wait a minute."},
                    status=429
                )

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
