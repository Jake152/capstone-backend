"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from backend.views.clientView import ClientListView, ClientView
from backend.views.routeView import RouteListView, RouteView
from backend.views.testView import TestView
from backend.views.locationView import LocationView, LocationListView
from backend.views.driverView import DriverView, DriverListView
from backend.views.managerView import ManagerView, ManagerListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('test/', TestView.as_view()),
    path('locations/', LocationListView.as_view()),
    path('locations/<int:pk>/', LocationView.as_view()),
    path('clients/', ClientListView.as_view()),
    path('clients/<int:pk>/', ClientView.as_view()),
    path('routes/', RouteListView.as_view()),
    path('routes/<int:pk>/', RouteView.as_view())
    path('drivers/', DriverListView.as_view()),
    path('drivers/<int:pk>/', DriverView.as_view()),
    path('managers/', ManagerListView.as_view()),
    path('managers/<int:pk>/', ManagerView.as_view())
]
