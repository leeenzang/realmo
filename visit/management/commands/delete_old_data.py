from django.core.management.base import BaseCommand
from visit.models import Visitor
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Delete data older than 3 months'

    def handle(self, *args, **kwargs):
        three_months_ago = datetime.today().date() - timedelta(days=90)
        deleted_count, _ = Visitor.objects.filter(사용일__lt=three_months_ago).delete()
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {deleted_count} records older than 3 months'))
