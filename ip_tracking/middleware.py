from django.utils.deprecation import MiddlewareMixin
from ipware import get_client_ip
from django.http import HttpResponseForbidden
from .models import RequestLog, BlockedIP


class LogRequestDetailsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip, _ = get_client_ip(request)
        ip_address = ip or "0.0.0.0"

        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            return HttpResponseForbidden("Access denied")

        RequestLog.objects.create(
            ip_address=ip_address,
            path=request.path,
        )

        return None