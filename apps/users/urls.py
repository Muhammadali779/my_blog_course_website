from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('course-login/', views.course_login_view, name='course_login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/users/', views.manage_users, name='manage_users'),
    path('dashboard/users/create/', views.create_user, name='create_user'),
    path('dashboard/users/<int:user_id>/role/', views.change_user_role, name='change_user_role'),
    path('dashboard/users/<int:user_id>/toggle/', views.toggle_user_active, name='toggle_user_active'),
]
