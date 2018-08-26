from django.urls import path, include
from .views import IssueListView, issues_csv


urlpatterns = [
    path('ideas/', IssueListView.as_view(), name='public-issue-list'),
    path('ideas/csv/', issues_csv, name='public-issue-csv')
]
