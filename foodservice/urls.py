from django.urls import path
from . import views

app_name = 'foodservice'

urlpatterns = [
    path('', views.group_type_list, name='group_type_list'),
    path('grouptype', views.group_type_list, name='group_type_list'),
    path('grouptype/<int:pk>', views.group_type_detail, name='group_type_detail'),
    path('grouptype/create', views.create_group_type, name='create_group_type'),
    path('grouptype/<int:pk>/edit', views.edit_group_type, name='edit_group_type'),
    path('group/<int:pk>', views.group_detail, name='group_detail'),
    path('group/create', views.create_group, name='create_group'),
    path('group/<int:pk>/edit', views.edit_group, name='edit_group'),
    path('group/<int:pk>/delete', views.delete_group, name='delete_group'),
    path('group/<int:pk>/prune', views.prune_group_bookings, name='prune_group_bookings'),
    path('groupsession', views.group_session_list, name='group_session_list'),
    path('groupsession/<int:pk>', views.group_session_detail, name='group_session_detail'),
    path('groupsession/create', views.create_group_session, name='create_group_session'),
    path('groupsession/createbulk', views.create_bulk_group_sessions, name='create_bulk_group_sessions'),
    path('groupsession/<int:pk>/edit', views.edit_group_session, name='edit_group_session'),
    path('groupsession/<int:pk>/delete', views.delete_group_session, name='delete_group_session'),
    path('groupsession/<int:pk>/addclient', views.add_group_session_attender, name='add_group_session_attender'),
    path('groupsession/<int:pk>/removeclient', views.remove_group_session_attender, name='remove_group_session_attender'),
    path('groupbooking/create', views.create_group_booking, name='create_group_booking'),
    path('groupbooking/<int:pk>/edit', views.edit_group_booking, name='edit_group_booking'),
    path('groupbooking/<int:pk>/delete', views.delete_group_booking, name='delete_group_booking'),
]
