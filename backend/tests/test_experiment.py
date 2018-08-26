from django.test import TestCase
from django.contrib.auth.models import User

from experiment.models import *
from random import seed
from collections import Counter
from experiment.treatments import auto_assign_user, assignment_stats


class TestExperiments(TestCase):
    def setUp(self):
        self.users = [
            User.objects.create_user(username='dominique'),
            User.objects.create_user(username='noriko'),
            User.objects.create_user(username='ralph'),
            User.objects.create_user(username='pearlene'),
            User.objects.create_user(username='wilma'),
            User.objects.create_user(username='bradley'),
            User.objects.create_user(username='tonette'),
            User.objects.create_user(username='delora'),
            User.objects.create_user(username='danita'),
            User.objects.create_user(username='kenneth')
        ]

    def test_classification(self):
        res = ClassificationResult(user=self.users[0],
            score_autonomy=5,
            score_impersonal=1,
            score_control=1,
            score_amotivation=1)
        # This is 100% autonomy
        self.assertEquals(res.calculate_group(), 'autonomy')

        res = ClassificationResult(user=self.users[0],
            score_autonomy=1,
            score_impersonal=5,
            score_control=1,
            score_amotivation=1)
        # This is 40% autonomy
        seed(20180330)
        cnt = Counter([res.calculate_group() for i in range(100)])
        self.assertEquals(cnt['control'], 59)
        self.assertEquals(cnt['autonomy'], 41)

    def test_asisgnment(self):
        versions = [
            Treatment.objects.create(name='autonomy', label='Autonomy-supportive', target_assignment_ratio=1/3),
            Treatment.objects.create(name='control', label='Control-supportive', target_assignment_ratio=1/3),
            Treatment.objects.create(name='baseline', label='Baseline', target_assignment_ratio=1/3)
        ]

        seed(2018033003)
        for u in self.users:
            res = ClassificationResult(user=u,
                score_autonomy=1,
                score_impersonal=5,
                score_control=1,
                score_amotivation=1)
            res.save()  # 40% autonomy. this seed yields 3 autonomy, 7 control users
            auto_assign_user(u)
        
        stats = assignment_stats()
        stats_by_name = {'%s/%s' % (obj['name'], obj['assignment__group']): {'target': obj['target_assignment_ratio'], 'ratio': obj['ratio'], 'count': obj['count']} for obj in stats}
        self.assertEquals(stats_by_name['autonomy/autonomy']['count'], 1)
        self.assertEquals(stats_by_name['autonomy/control']['count'],  3)
        self.assertEquals(stats_by_name['baseline/autonomy']['count'], 1)
        self.assertEquals(stats_by_name['baseline/control']['count'],  2)
        self.assertEquals(stats_by_name['control/autonomy']['count'],  1)
        self.assertEquals(stats_by_name['control/control']['count'],   2)

