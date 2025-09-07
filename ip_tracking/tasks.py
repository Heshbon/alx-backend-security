from celery import shared_task
from datetime import timedelta
from django.db.models import Count
from django.utils import timezone
from .models import RequestLog, SuspiciousIP

SENSITIVE_PATHS = ['/admin/', '/login/']
THRESHOLD = 100


@shared_task
def detect_suspicious_activity():
    now = timezone.now()
    one_hour_ago = now - timedelta(hours=1)

    # IPs detection threshold
    high_traffic_ips = (
        RequestLog.objects
        .filter(timestamp__gte=one_hour_ago)
        .values('ip_address')
        .annotate(request_count=Count('id'))
        .filter(request_count__gt=THRESHOLD)
    )

    for entry in high_traffic_ips:
        ip = entry['ip_address']
        reason = f"Excessive requests ({entry['request_count']}/hour)"
        SuspiciousIP.objects.update_or_create(
            ip_address=ip, defaults={'reason': reason})

    # IPs detecting sensitive paths
    sensitive_ips = (
        RequestLog.objects
        .filter(timestamp__gte=one_hour_ago, path__in=SENSITIVE_PATHS)
        .values('ip_address')
        .annotate(count=Count('id'))
    )

    for entry in sensitive_ips:
        ip = entry['ip_address']
        reason = f"Accessed sensitive paths: {SENSITIVE_PATHS}"
        SuspiciousIP.objects.update_or_create(
            ip_address=ip, defaults={'reason': reason})