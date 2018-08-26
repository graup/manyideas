from .models import Treatment, Assignment, ClassificationResult
from django.db.models import Count, Max, Q
from operator import itemgetter

def get_active_treatments():
    return Treatment.active_treatments.all()

def get_default_treatment():
    t, _ = Treatment.objects.get_or_create(name='default', defaults={'label': 'default', })
    return t

def assignment_stats():
    # Get current assignment counts
    all_treatments = Treatment.objects.filter(target_assignment_ratio__gt=0).values('name').all()
    current_assignments = Assignment.objects.order_by().values('user_id').annotate(max_id=Max('id')).values('max_id')
    counts = Treatment.objects.filter(target_assignment_ratio__gt=0).values(
        'id', 'target_assignment_ratio', 'name', 'label', 'assignment__group'
    ).annotate(count=Count('assignment', filter=Q(assignment__id__in=current_assignments), distinct=True))

    counts = list(counts)
    treatments_by_name = {c['name']: c for c in counts}

    # Add missing groups
    existing_splits = set([(c['name'], c['assignment__group']) for c in counts])
    all_splits = set([(t['name'], g) for t in all_treatments for g in Assignment.GROUPS])
    missing_splits = all_splits - existing_splits
    counts += [{
        'name': s[0],
        'assignment__group': s[1],
        'count': 0,
        'id': treatments_by_name[s[0]]['id'],
        'target_assignment_ratio': treatments_by_name[s[0]]['target_assignment_ratio'],
        'label': treatments_by_name[s[0]]['label']
    } for s in missing_splits]

    # Compute ratio distances
    total_assignments = sum([c['count'] for c in counts])
    for c in counts:
        c.update(target_assignment_ratio=c['target_assignment_ratio']/Assignment.NUM_GROUPS)
        if total_assignments == 0:
            c.update(ratio=0, new_ratio=0)
        else:
            c.update(ratio=c['count']/total_assignments)  # current ratio
            c.update(new_ratio=(1+c['count'])/total_assignments)  # ratio after updating
        c.update(ratio_distance=c['target_assignment_ratio']-c['new_ratio'])  # difference after updating
        c.update(display_ratio=c['ratio']-abs(min(0, c['ratio_distance'])))
    xstr = lambda s: s if s else ''
    return sorted(counts, key=lambda item: tuple(map(xstr, itemgetter('assignment__group', 'name')(item))))

def get_auto_treatment(group=None):
    # Get treatment that this user would be auto-assigned to
    stats = assignment_stats()
    if group:
        stats = filter(lambda item: item['assignment__group'] == group or item['assignment__group'] is None, stats)
    else:
        stats = filter(lambda item: item['assignment__group'] is not None, stats)
    return max(stats, key=itemgetter('ratio_distance'))

def auto_assign_user(user, group=None):
    """Assign user to a treatment, satisfying the treatment assignment target ratios for (treatment, group)"""
    if not group:
        try:
            result = ClassificationResult.objects.filter(user=user)[0]
            group = result.calculated_group
        except IndexError:
            pass
    treatment = get_auto_treatment(group)
    if not group:
        group = treatment['assignment__group']
    assignment = Assignment(treatment_id=treatment['id'], user=user, group=group)
    assignment.save()
    return assignment

