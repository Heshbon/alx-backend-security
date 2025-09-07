# IP Tracking: Security and Analytics

A Django application implementing comprehensive IP tracking with security features and analytics capabilities.

## Features

* IP logging with request metadata
* Blacklist management system
* Geolocation integration with caching
* Rate limiting for authenticated/unauthenticated users
* Anomaly detection with scheduled tasks
* GDPR/CCPA compliance support

## Requirements

* Python 3.10+
* Django 4.2+
* Redis server
* Celery worker
* django-ratelimit
* django-ipgeolocation

## Installation

```bash
pip install -r requirements.txt
python manage.py migrate
```

## Configuration

Add to settings.py:

```python
MIDDLEWARE = [
    'ip_tracking.middleware.LogRequestDetailsMiddleware',
]

INSTALLED_APPS = [
    'ip_tracking',
    'django_ratelimit',
]

CELERY_BEAT_SCHEDULE = {
    'detect-suspicious-activity': {
        'task': 'ip_tracking.tasks.detect_suspicious_activity',
        'schedule': '*/60', # every hr
    },
}
```

## Usage

1. Start Redis:
```bash
redis-server
```

2. Start Celery worker:
```bash
celery -A ip_tracking worker --beat --scheduler django --loglevel=info
```

3. Block IP address:
```bash
python manage.py block_ip --ip 203.0.113.9
```

## Monitoring

Access the admin interface to monitor:
- Request logs.
- Blocked IPs.
- Suspicious activity.
- System status.

## Privacy Considerations

This implementation follows privacy best practices:

* IP addresses are stored temporarily.
* Logs are automatically cleaned up after retention period.
* Users can opt-out of tracking.
* Data is anonymized when possible.

## License

MIT License

Copyright (c) 2025 Hesbon Kipchirchir

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.