from django.urls import path
from . import views

app_name = 'foodbank'

urlpatterns = [
    path('', views.foodbank_referral_today, name='foodbank_referral_today'),
    path('referral', views.foodbank_referral_list, name='foodbank_referral_list'),
    path('referral/<int:pk>/edit', views.edit_foodbank_referral, name='edit_foodbank_referral'),
    path('referral/create', views.create_foodbank_referral, name='create_foodbank_referral'),
    path('referral/<int:pk>/delete', views.delete_foodbank_referral, name='delete_foodbank_referral'),
]
