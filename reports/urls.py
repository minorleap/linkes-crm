from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.client_report, name='client_report'),
    path('clients', views.client_report, name='client_report'),
    path('timesheets', views.timesheet_report, name='timesheet_report'),
]
