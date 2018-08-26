from django.views.generic.list import ListView
from django.utils import timezone
from django.db.models import Count, Q
from django.http import HttpResponse
from django.utils.timezone import now

import csv

from .models import Issue

class IssueListView(ListView):
    model = Issue

    def get_queryset(self):
        qs = Issue.available_objects.prefetch_related('comment_set')
        qs = qs.annotate(like_count=Count('tag_set', filter=Q(tag_set__kind=0), distinct=True))
        qs = qs.annotate(comment_count=Count('comment', filter=Q(comment__deleted_date__isnull=True), distinct=True))
        return qs.order_by('-like_count', '-comment_count')


def issues_csv(request):
    header = ['id', 'title', 'created_date', 'like_count', 'comment_count']

    dl = True
    ct = "text/csv" if dl else "text/plain"
    response = HttpResponse(content_type=ct)
    filename = 'issues_%s.csv' % now().isoformat()[:16].replace(':', '-')
    if dl:
        response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    writer = csv.DictWriter(response, fieldnames=header, restval=0)
    writer.writer.writerow(writer.fieldnames)
    
    data = IssueListView.get_queryset(None).values(*header)
    writer.writerows(data)
    return response