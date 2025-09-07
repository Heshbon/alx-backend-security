from django.utils.deprecation import MiddlewareMixin
from ipware import get_client_ip
from django.http import HttpResponseForbidden
from django.core.cache import cache
from .models import RequestLog, BlockedIP
import requests
from datetime import timedelta

GEOLOCATION_CACHE_TIMEOUT = timedelta(hours=24).total_seconds()


def get_geolocation_data(ip_address):
    cache_key = f"geo:{ip_address}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data

    try:
        api_url = f'https://ipapi.co/{ip_address}/json/'
        response = requests.get(api_url)
        if response.status_code == 200:
            geo_data = response.json()
            cache.set(cache_key, geo_data, GEOLOCATION_CACHE_TIMEOUT)
            return geo_data
    except Exception:
        pass

    return None


class LogRequestDetailsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip, _ = get_client_ip(request)
        ip_address = ip or "0.0.0.0"

        # Block blacklisted IPs
        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            return HttpResponseForbidden("Access denied")

        # Request log
        request_log = RequestLog.objects.create(
            ip_address=ip_address, path=request.path)

        # Geolocation and update log
        geo_data = get_geolocation_data(ip_address)
        if geo_data:
            RequestLog.objects.filter(pk=request_log.pk).update(
                country=geo_data.get('country_name', ''),
                city=geo_data.get('city', '')
            )

        return None