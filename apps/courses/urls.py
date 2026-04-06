from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('manage/', views.manage_courses, name='manage_courses'),
    path('create/', views.course_create, name='course_create'),
    path('enrollments/', views.manage_enrollments, name='manage_enrollments'),
    path('enrollments/<int:enrollment_id>/payment/', views.update_payment, name='update_payment'),
    path('<slug:slug>/', views.course_detail, name='course_detail'),
    path('<slug:slug>/enroll/', views.enroll_course, name='enroll_course'),
    path('<slug:slug>/edit/', views.course_edit, name='course_edit'),
    path('<slug:slug>/delete/', views.course_delete, name='course_delete'),
    path('<slug:slug>/modules/', views.course_modules, name='course_modules'),
    path('<slug:slug>/students/', views.manage_students, name='manage_students'),
    path('<slug:course_slug>/lessons/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
]
