from django.urls import path
from . import views

app_name = 'foodshopping'

urlpatterns = [
    path('', views.shopping_delivery_today, name='shopping_delivery_today'),
    path('shoppingdelivery', views.shopping_delivery_list, name='shopping_delivery_list'),
    path('shoppingdelivery/<int:pk>/edit', views.edit_shopping_delivery, name='edit_shopping_delivery'),
    path('shoppingdelivery/create', views.create_shopping_delivery, name='create_shopping_delivery'),
    path('shoppingdelivery/<int:pk>/delete', views.delete_shopping_delivery, name='delete_shopping_delivery'),
    path('shoppingdelivery/generate/<str:datestring>', views.generate_shopping_deliveries, name='generate_shopping_deliveries'),
    path('shoppingdelivery/export/<str:datestring>', views.export_shopping_deliveries, name='export_shopping_deliveries'),
    path('shoppingschedule/<int:pk>/edit', views.edit_shopping_schedule, name='edit_shopping_schedule'),
    path('shoppingschedule/create', views.create_shopping_schedule, name='create_shopping_schedule'),
    path('exceptiondate/create', views.create_exception_date, name='create_exception_date'),
    path('exceptiondate/<int:pk>/delete', views.delete_exception_date, name='delete_exception_date'),
    path('misseddeliverydate/create', views.create_missed_delivery_date, name='create_missed_delivery_date'),
    path('misseddeliverydate/<int:pk>/delete', views.delete_missed_delivery_date, name='delete_missed_delivery_date'),
]
