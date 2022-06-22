from django.urls import path
from . import views

app_name = 'child'

urlpatterns = [
    path('', views.child_list, name='child_list'),
    path('<int:pk>', views.child_detail, name='child_detail'),
    path('<int:pk>/edit', views.edit_child, name='edit_child'),
    path('create', views.create_child, name='create_child'),
]
