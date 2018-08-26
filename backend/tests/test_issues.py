from django.test import TestCase
from django.contrib.auth.models import User

from issues.models import *


class TestIssues(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alice')
        self.user2 = User.objects.create_user(username='bob')
        self.categories = {
            'spaces': Category.objects.create(label='Spaces')
        }

    def test_categories(self):
        self.assertEquals(self.categories['spaces'].slug, 'spaces')
  
    def test_basics(self):
        issue = Issue(
            title="More room for group project meetings",
            text="A longer description of the issue at hand.",
            author=self.user
        )
        issue.save()
        issue.categories.set([self.categories['spaces']])
