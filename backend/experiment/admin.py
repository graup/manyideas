from django.contrib import admin
from .models import Treatment, Assignment, ClassificationResult

class TreatmentAdmin(admin.ModelAdmin):
    model = Treatment
    list_display = ('name', 'label', 'is_active', 'target_assignment_ratio',)
admin.site.register(Treatment, TreatmentAdmin)

class AssignmentAdmin(admin.ModelAdmin):
    model = Assignment
    list_display = ('user', 'group', 'treatment', 'assigned_date',)
admin.site.register(Assignment, AssignmentAdmin)

class ClassificationResultAdmin(admin.ModelAdmin):
    model = ClassificationResult
    list_display = (
        'user', 'calculated_group', 'age', 'sex', 'occupation',
        'score_autonomy', 'score_impersonal', 'score_control', 'score_amotivation',
        'completed_date'
    )
admin.site.register(ClassificationResult, ClassificationResultAdmin)
