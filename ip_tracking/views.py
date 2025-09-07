# ip_tracking/views.py
from django.contrib.auth.decorators import login_required
from django_ratelimit.decorators import ratelimit
from django.http import HttpResponse
from django.views.decorators.cache import cache_page


@login_required
@ratelimit(key='user_or_ip', rate='10/m', method=['GET', 'POST'],
           block=True, cache_timeout=300)
def protected_view(request):
    return HttpResponse("Protected content")


@ratelimit(key='user_or_ip', rate='5/m', method=['GET', 'POST'],
           block=True, cache_timeout=300)
def public_view(request):
    return HttpResponse("Public content")