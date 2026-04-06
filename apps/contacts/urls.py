from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact_view, name='contact'),
    path('messages/', views.contact_list, name='contact_list'),
    path('messages/<int:pk>/read/', views.mark_read, name='mark_read'),
    path('settings/', views.site_settings_view, name='site_settings'),
]
