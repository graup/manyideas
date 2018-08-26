from django.views.generic.base import TemplateView
from django.urls import reverse
from django import forms
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.db.models import Max
from django.contrib import admin
from django.db.models import Count, Q
from django.db.models.functions import TruncDay
from rest_framework.exceptions import PermissionDenied
import csv
from django.http import StreamingHttpResponse, HttpResponse
from django.utils.timezone import now
from .models import Assignment, Treatment
from .treatments import get_default_treatment, auto_assign_user, assignment_stats, get_auto_treatment
from issues.models import Issue, Comment, Tag
import pytz
from collections import defaultdict
from operator import itemgetter


class Echo:
    def write(self, value):
        return value

def data_export_csv_view(request):
    if not request.user.is_superuser: 
        raise PermissionDenied()

    header = ['id', 'username', 'group', 'treatment', 'occupation', 'sex', 'age', 'issue_count', 'comment_count', 'like_count', 'flag_count', 'like_received_count', 'avg_issue_length']

    def get_row(user):
        like_counts = user.issue_set.annotate(like_count=Count('tag_set', filter=Q(tag_set__kind=0))).values_list('like_count')
        like_received_count = sum([a[0] for a in like_counts])
        issue_count = user.issue_set.count()
        issue_length = sum([sum(list(map(len, v))) for v in user.issue_set.values_list('text', 'title')])
        avg_issue_length = 0
        if issue_count > 0:
            avg_issue_length = round(issue_length/issue_count, 2)
        dt = {
            'id': user.id,
            'username': user.username,
            'issue_count': issue_count,
            'comment_count': user.comment_set.count(),
            'like_count': user.tag_set.filter(kind=0).count(),
            'like_received_count': like_received_count,
            'flag_count': user.tag_set.filter(kind=1).count(),
            'avg_issue_length': avg_issue_length
        }
        try:
            classification = user.classificationresult_set.order_by('-completed_date')[0]
            assignment = user.assignment_set.order_by('-assigned_date')[0]
        except IndexError:
            return dt

        dt.update({
            'group': classification.calculated_group,
            'treatment': assignment.treatment.name,
            'age': classification.age,
            'sex': classification.sex,
            'occupation': classification.occupation,
        })
        return dt

    def iter_items(items, pseudo_buffer):
        writer = csv.DictWriter(pseudo_buffer, fieldnames=header)
        yield writer.writer.writerow(writer.fieldnames)

        for item in items:
            yield writer.writerow(get_row(item))

    response = StreamingHttpResponse(
        streaming_content=(iter_items(User.objects.all(), Echo())),
        content_type="text/csv"
    )
    filename = 'data_%s.csv' % now().isoformat()[:16].replace(':', '-')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    return response


def stats_export_csv_view(request):
    if not request.user.is_superuser: 
        raise PermissionDenied()

    header = ['date', 'signups', 'issue_count', 'comment_count']

    tz = pytz.timezone('Asia/Seoul')

    response = HttpResponse(content_type="text/csv")
    filename = 'stats_%s.csv' % now().isoformat()[:16].replace(':', '-')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    writer = csv.DictWriter(response, fieldnames=header, restval=0)
    writer.writer.writerow(writer.fieldnames)
    user_stats = User.objects.all().filter(
        assignment__isnull=False
    ).annotate(
        date=TruncDay('date_joined',  tzinfo=tz)
    ).order_by('date').values('date').annotate(
        signups=Count('id', distinct=True)
    )
    issue_stats = Issue.objects.all().annotate(
        date=TruncDay('created_date',  tzinfo=tz)
    ).order_by('date').values('date').annotate(
        issue_count=Count('id', distinct=True)
    )
    comment_stats = Comment.objects.all().annotate(
        date=TruncDay('created_date',  tzinfo=tz)
    ).order_by('date').values('date').annotate(
        comment_count=Count('id', distinct=True)
    )
    merged_stats = defaultdict(dict)
    for stat in (user_stats, issue_stats, comment_stats,):
        for row in stat:
            row['date'] = row['date'].date()
            merged_stats[row['date']].update(row)
    merged_stats = sorted(merged_stats.values(), key=itemgetter('date'))
    writer.writerows(merged_stats)
    return response

class AssignmentForm(forms.ModelForm):
    treatment = forms.ModelChoiceField(queryset=Treatment.objects, widget=forms.RadioSelect, required=False)
    auto_assign = forms.BooleanField(required=False)
    group = forms.ChoiceField(choices=[(None, '(None)')]+[(g, g) for g in Assignment.GROUPS], required=False)

    class Meta:
        model = Assignment
        fields = ['user', 'group', 'treatment', 'auto_assign']

class AssignmentUpdateView(TemplateView):
    model = Assignment
    form_class = AssignmentForm
    template_name = "experiment/AssignmentUpdateView.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get latest assignment for each user
        qs = Assignment.objects.filter(pk__in=
            Assignment.objects.order_by().values('user_id').annotate(
                max_id=Max('id')
            ).values('max_id')
        ).order_by('group', 'treatment', 'user')
        # Get unassigned users
        unassigned_users = User.objects.exclude(pk__in=qs.values('user_id')).values('id', 'username')
        initials = [{'user': u['id']} for u in unassigned_users]

        # Generate formset
        AssignmentFormSet = forms.modelformset_factory(Assignment, form=AssignmentForm, extra=len(initials))
        if self.request.POST:
            context['formset'] = AssignmentFormSet(self.request.POST, queryset=qs, initial=initials)
        else:
            context['formset'] = AssignmentFormSet(queryset=qs, initial=initials)
        # Add Django Admin context
        context.update(admin.site.each_context(self.request))
        # Add stats
        stats = assignment_stats()
        context.update(
            stats=stats,
            next_assignments=[get_auto_treatment(g) for g in Assignment.GROUPS],
            total_n=sum([t['count'] for t in stats])
        )
        return context

    def post(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data.get('auto_assign', False):
                    auto_assign_user(form.cleaned_data['user'], form.cleaned_data['group'])
                elif form.cleaned_data.get('treatment', False):
                    form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data())

    def get_success_url(self):
        return reverse('treatment-assignments')

