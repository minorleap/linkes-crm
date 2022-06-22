"""linkes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import client.views


urlpatterns = [
    path('', client.views.client_list, name='client_list'),
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('client/', include('client.urls')),
    path('child/', include('child.urls')),
    path('meals/', include('meals.urls')),
    path('foodshopping/', include('foodshopping.urls')),
    path('halalshopping/', include('halalshopping.urls')),
    path('phonecalls/', include('phonecalls.urls')),
    path('staff/', include('staff.urls')),
    path('group/', include('group.urls')),
    path('childrensgroup/', include('childrensgroup.urls')),
    path('foodbank/', include('foodbank.urls')),
    path('foodhub/', include('foodhub.urls')),
    path('reports/', include('reports.urls')),
    path('foodservice/', include('foodservice.urls')),
]
