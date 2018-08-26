from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from issues.models import Issue


class Command(BaseCommand):
    help = 'Recalculate heat scores for all issues'
    # cd ~/thesis-experiment/thesis-experiment/backend/; workon backend; python manage.py recalculate_heat

    def handle(self, *args, **options):
        qs = Issue.objects
        paginator = Paginator(qs.all(), 20)

        for page in range(1, paginator.num_pages + 1):
            for row in paginator.page(page).object_list:
                row.save()

        self.stdout.write(self.style.SUCCESS('Updated {} issues'.format(qs.count())))