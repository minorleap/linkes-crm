from django.urls import path
from . import views

app_name = 'meals'

urlpatterns = [
    path('', views.meal_delivery_today, name='meal_delivery_today'),
    path('mealdelivery', views.meal_delivery_list, name='meal_delivery_list'),
    path('mealdelivery/<int:pk>/edit', views.edit_meal_delivery, name='edit_meal_delivery'),
    path('mealdelivery/create', views.create_meal_delivery, name='create_meal_delivery'),
    path('mealdelivery/<int:pk>/delete', views.delete_meal_delivery, name='delete_meal_delivery'),
    path('mealdelivery/generate/<str:datestring>', views.generate_meal_deliveries, name='generate_meal_deliveries'),
    path('mealdelivery/export/<str:datestring>', views.export_meal_deliveries, name='export_meal_deliveries'),
    path('mealschedule/<int:pk>/edit', views.edit_meal_schedule, name='edit_meal_schedule'),
    path('mealschedule/create', views.create_meal_schedule, name='create_meal_schedule'),
    path('exceptiondate/create', views.create_exception_date, name='create_exception_date'),
    path('exceptiondate/<int:pk>/delete', views.delete_exception_date, name='delete_exception_date'),
    path('misseddeliverydate/create', views.create_missed_delivery_date, name='create_missed_delivery_date'),
    path('misseddeliverydate/<int:pk>/delete', views.delete_missed_delivery_date, name='delete_missed_delivery_date'),
]
