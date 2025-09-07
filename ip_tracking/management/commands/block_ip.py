from django.core.management.base import BaseCommand, CommandError
from ipaddress import ip_address as ip_validator
from ...models import BlockedIP


class Command(BaseCommand):
    help = 'Block an IP address'

    def add_arguments(self, parser):
        parser.add_argument('ip', type=str, help='IP address to block')

    def handle(self, *args, **options):
        ip_str = options['ip']
        try:
            # IP validate
            ip_validator(ip_str)

            if BlockedIP.objects.filter(ip_address=ip_str).exists():
                self.stdout.write(self.style.WARNING(
                    f'IP {ip_str} is already blocked.'))
            else:
                BlockedIP.objects.create(ip_address=ip_str)
                self.stdout.write(self.style.SUCCESS(f'Blocked IP: {ip_str}'))

        except ValueError:
            raise CommandError(f'Invalid IP address: {ip_str}')