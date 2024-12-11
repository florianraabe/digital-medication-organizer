"""
URL configuration for MedApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path('calendar/', views.calendar_month, name="calendar"),
    path('calendar/<int:year>/<int:month>/', views.calendar_month, name="calendar"),
    path('calendar/<int:year>/<int:month>/<int:day>/', views.mark_calendar_day, name="mark-calendar-day"),
    path('medication/', views.MedicationListView.as_view(), name="medication"),
    path('medication/<int:pk>/', views.MedicationDetailView.as_view(), name="detail-medication"),
    path('medication/add/', views.MedicationCreateView.as_view(), name="add-medication"),
    path('medication/edit/<int:pk>/', views.MedicationUpdateView.as_view(), name="edit-medication"),
    path('medication/delete/<int:pk>/', views.MedicationDeleteView.as_view(), name="delete-medication"),
    path('perception/', views.PerceptionListView.as_view(), name="perception"),
    path('perception/add/', views.PerceptionCreateView.as_view(), name="add-perception"),
    path('export/', views.export, name="export"),
    path('track/<int:time>/<int:click>/<int:x>/<int:y>/<int:w>/<int:h>/<path:src>/', views.track_mouse, name="track"),
]
