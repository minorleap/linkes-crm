from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    path('', views.staff_list, name='staff_list'),
    path('<int:pk>', views.staff_detail, name='staff_detail'),
    path('<int:pk>/edit', views.edit_staff, name='edit_staff'),
    path('create', views.create_staff, name='create_staff'),
    path('role/create', views.create_role, name='create_role'),
    path('role/<int:pk>/delete', views.delete_role, name='delete_role'),
    path('timesheet', views.timesheet_list, name='timesheet_list'),
]
