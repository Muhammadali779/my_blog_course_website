from django.contrib import admin
from .models import Course, Module, Lesson, Enrollment, Category, LessonProgress


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'instructor', 'is_free', 'price', 'is_published', 'created_at']
    list_filter = ['is_free', 'is_published', 'level']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order']
    inlines = [LessonInline]


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'payment_status', 'enrolled_at', 'is_active']
    list_filter = ['payment_status', 'is_active']
    list_editable = ['payment_status', 'is_active']
