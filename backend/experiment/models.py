from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.urls import reverse
from config.utils import notify_slack
from random import random


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Treatment(models.Model):
    name = models.SlugField(unique=True)
    label = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    target_assignment_ratio = models.FloatField(default=0)

    objects = models.Manager()
    active_treatments = ActiveManager()

    def __str__(self):
        return self.label

    class Meta:
        ordering = ('name',)


class Assignment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.CharField(max_length=10, blank=True, null=True)
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE)
    assigned_date = models.DateTimeField(auto_now_add=True)

    GROUPS = ('autonomy', 'control', )
    NUM_GROUPS = len(GROUPS)

    __treatment_id = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__treatment_id = self.treatment_id

    def __str__(self):
        return '%s - %s/%s' % (self.user, self.treatment.name, self.group)

    def save(self, *args, **kwargs):
        if self.treatment_id != self.__treatment_id:
            # Force creation of new item
            self.pk = None
        super().save(*args, **kwargs)


def notify_assignment(sender, instance, created, **kwargs):
    from .treatments import assignment_stats
    if not created:
        return
    content_type = ContentType.objects.get_for_model(instance.__class__)
    url = reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(instance.pk,))
    stats = assignment_stats()
    stats_text = ', '.join(['%s/%s N=%d (%d%%)' % (s['name'], s['assignment__group'], s['count'], 100*s['ratio']) for s in stats if s['count'] > 0])
    notify_slack('*New assignment!* %s \n Stats: %s \n' % (instance, stats_text), url)
post_save.connect(notify_assignment, sender=Assignment)

class ClassificationResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    completed_date = models.DateField(auto_now_add=True)
    score_autonomy = models.IntegerField()
    score_impersonal = models.IntegerField()
    score_control = models.IntegerField()
    score_amotivation = models.IntegerField()
    calculated_group = models.CharField(max_length=10, blank=True, null=True)

    age = models.CharField(max_length=10)
    sex = models.CharField(max_length=10)
    occupation = models.CharField(max_length=10)

    class Meta:
        ordering = ('-id',)

    def calculate_group(self):
        "Calculate group based on Inference Tree computed from Mturk data"
        prob_autonomy = 0
        if self.score_amotivation <= 3:  # 2 on 5-scale likert -> 3 on 7-scale likert
            if self.score_impersonal <= 3:
                if self.score_control <= 2:
                    prob_autonomy = 1.0  # Autonomy with 0% error
                else:
                    if self.score_autonomy <= 5:
                        prob_autonomy = 0.5  # Control with 50% error
                    else:
                        prob_autonomy = 0.9  # Autonomy with 10% error
            else:
                prob_autonomy = 0.41  # Control with 41% error
        else:
            prob_autonomy = 0.09  # Control with 9% error
        if random() < prob_autonomy:
            return 'autonomy'
        return 'control'

    def save(self, *args, **kwargs):
        # Calculate group
        if not self.calculated_group:
            self.calculated_group = self.calculate_group()
        super().save(*args, **kwargs)


class GcosResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    completed_date = models.DateField(auto_now_add=True)
    score_autonomy = models.IntegerField()
    score_control = models.IntegerField()
    score_impersonal = models.IntegerField()
    score_order = models.CharField(max_length=3)

    @property
    def scores(self):
        return {
            'A': self.score_autonomy,
            'C': self.score_control,
            'I': self.score_impersonal
        }
    
    def _calculate_score_order(self):
        scores_sorted = sorted(self.scores.items(), key=lambda item: item[1])[::-1]
        return ''.join([item[0] for item in test_scores_sorted])

    def save(self, *args, **kwargs):
        self.score_order = self._calculate_score_order()
        super().save(*args, **kwargs)

    def __str__(self):
        return 'A %d, C %d, I %d' % (self.score_autonomy, self.score_control, self.score_impersonal)