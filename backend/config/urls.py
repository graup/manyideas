from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('api.urls')),
    path('', include('experiment.urls')),
    path('', include('issues.urls')),
    path('admin/', admin.site.urls),
]
