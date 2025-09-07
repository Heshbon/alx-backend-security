from django.utils.deprecation import MiddlewareMixin
from ipware import get_client_ip
from .models import RequestLog


class LogRequestDetailsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip, _ = get_client_ip(request)
        ip_address = ip or "0.0.0.0"

        RequestLog.objects.create(
            ip_address=ip_address,
            path=request.path,
        )
        return None