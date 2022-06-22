from django.urls import path
from . import views

app_name = 'phonecalls'

urlpatterns = [
    path('', views.phonecall_today, name='phonecall_today'),
    path('phonecall', views.phonecall_list, name='phonecall_list'),
    path('phonecall/<int:pk>/edit', views.edit_phonecall, name='edit_phonecall'),
    path('phonecall/create', views.create_phonecall, name='create_phonecall'),
    path('phonecall/<int:pk>/delete', views.delete_phonecall, name='delete_phonecall'),
    path('phonecall/generate/<str:datestring>', views.generate_phonecalls, name='generate_phonecalls'),
    path('phonecall/export/<str:datestring>', views.export_phonecalls, name='export_phonecalls'),
    path('phonecallschedule/<int:pk>/edit', views.edit_phonecall_schedule, name='edit_phonecall_schedule'),
    path('phonecallschedule/create', views.create_phonecall_schedule, name='create_phonecall_schedule'),
    path('exceptiondate/create', views.create_exception_date, name='create_exception_date'),
    path('exceptiondate/<int:pk>/delete', views.delete_exception_date, name='delete_exception_date'),
    path('missedcalldate/create', views.create_missed_call_date, name='create_missed_call_date'),
    path('missedcalldate/<int:pk>/delete', views.delete_missed_call_date, name='delete_missed_call_date'),
    path('phonecallnotes/create', views.create_phonecall_notes, name='create_phonecall_notes'),
    path('phonecallnotes/<int:pk>/delete', views.delete_phonecall_notes, name='delete_phonecall_notes'),    
]
