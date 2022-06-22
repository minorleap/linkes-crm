from django.urls import path
from . import views

app_name = 'foodhub'

urlpatterns = [
    path('', views.foodhub_collection_today, name='collection_today'),
    path('collection', views.foodhub_collection_list, name='collection_list'),
    path('collection/<int:pk>/edit', views.edit_foodhub_collection, name='edit_collection'),
    path('collection/create', views.create_foodhub_collection, name='create_collection'),
    path('collection/<int:pk>/delete', views.delete_foodhub_collection, name='delete_collection'),
]
