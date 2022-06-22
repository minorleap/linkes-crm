from django.urls import path
from . import views

app_name = 'client'

urlpatterns = [
    path('', views.client_list, name='client_list'),
    path('<int:pk>', views.client_detail, name='client_detail'),
    path('<int:pk>/edit', views.edit_client, name='edit_client'),
    path('create', views.create_client, name='create_client'),
    path('referral/create', views.create_referral, name='create_referral'),
    path('referral/<int:pk>/delete', views.delete_referral, name='delete_referral'),
    path('casenote/create', views.create_casenote, name='create_casenote'),
    path('casenote/<int:pk>/edit', views.edit_casenote, name='edit_casenote'),
    path('casenote/<int:pk>/delete', views.delete_casenote, name='delete_casenote'),
]
