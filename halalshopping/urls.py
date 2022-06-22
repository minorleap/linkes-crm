from django.urls import path
from . import views

app_name = 'halalshopping'

urlpatterns = [
    path('', views.shopping_collection_today, name='shopping_collection_today'),
    path('shoppingcollection', views.shopping_collection_list, name='shopping_collection_list'),
    path('shoppingcollection/<int:pk>/edit', views.edit_shopping_collection, name='edit_shopping_collection'),
    path('shoppingcollection/create', views.create_shopping_collection, name='create_shopping_collection'),
    path('shoppingcollection/<int:pk>/delete', views.delete_shopping_collection, name='delete_shopping_collection'),
    path('shoppingcollection/generate/<str:datestring>', views.generate_shopping_collections, name='generate_shopping_collections'),
    path('shoppingcollection/export/<str:datestring>', views.export_shopping_collections, name='export_shopping_collections'),
    path('shoppingschedule/<int:pk>/edit', views.edit_shopping_schedule, name='edit_shopping_schedule'),
    path('shoppingschedule/create', views.create_shopping_schedule, name='create_shopping_schedule'),
    path('exceptiondate/create', views.create_exception_date, name='create_exception_date'),
    path('exceptiondate/<int:pk>/delete', views.delete_exception_date, name='delete_exception_date'),
    path('missedcollectiondate/create', views.create_missed_collection_date, name='create_missed_collection_date'),
    path('missedcollectiondate/<int:pk>/delete', views.delete_missed_collection_date, name='delete_missed_collection_date'),
]
