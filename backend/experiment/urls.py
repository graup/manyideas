from django.contrib import admin
from django.urls import path, include
from .views import AssignmentUpdateView, data_export_csv_view, stats_export_csv_view
from django.contrib.admin.views.decorators import staff_member_required


urlpatterns = [
    path('admin/treatment-assignments', staff_member_required(AssignmentUpdateView.as_view()), name='treatment-assignments'),
    path('admin/export.csv', data_export_csv_view, name='export-data-csv'),
    path('admin/stats.csv', stats_export_csv_view, name='export-stats-csv'),
]
