import os
from datetime import datetime
import logging

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
