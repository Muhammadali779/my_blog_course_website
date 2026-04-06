from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Course, Module, Lesson, Enrollment, LessonProgress, Category
from .forms import CourseForm, ModuleForm, LessonForm


def course_list(request):
    courses = Course.objects.filter(is_published=True).prefetch_related('modules')
    cat_slug = request.GET.get('cat')
    selected_cat = None
    if cat_slug:
        selected_cat = get_object_or_404(Category, slug=cat_slug)
        courses = courses.filter(category=selected_cat)
    paginator = Paginator(courses, 6)
    page = request.GET.get('page', 1)
    return render(request, 'courses/course_list.html', {
        'courses': paginator.get_page(page),
        'categories': Category.objects.all(),
        'selected_cat': selected_cat,
    })


def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    modules = course.modules.prefetch_related('lessons').all()
    is_enrolled = False
    enrollment = None
    if request.user.is_authenticated:
        enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
        is_enrolled = enrollment is not None and enrollment.is_active
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'modules': modules,
        'is_enrolled': is_enrolled,
        'enrollment': enrollment,
    })


def enroll_course(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    if not request.user.is_authenticated:
        return redirect(f'/users/course-login/?next=/courses/{slug}/enroll/')
    existing = Enrollment.objects.filter(user=request.user, course=course).first()
    if existing:
        messages.info(request, "Siz allaqachon bu kursga yozilgansiz!")
        return redirect('course_detail', slug=slug)
    payment_status = 'free' if course.is_free else 'pending'
    Enrollment.objects.create(
        user=request.user,
        course=course,
        payment_status=payment_status,
        payment_amount=0 if course.is_free else course.price,
    )
    if request.user.role == 'user':
        request.user.role = 'student'
        request.user.save()
    messages.success(request, f"'{course.title}' kursiga muvaffaqiyatli yozildingiz!")
    return redirect('course_detail', slug=slug)


def lesson_detail(request, course_slug, lesson_id):
    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    lesson = get_object_or_404(Lesson, id=lesson_id, module__course=course)

    if not lesson.is_preview:
        if not request.user.is_authenticated:
            return redirect(f'/users/course-login/?next=/courses/{course_slug}/lessons/{lesson_id}/')
        if not request.user.is_student():
            messages.error(request, "Bu darsni ko'rish uchun kursga yoziling!")
            return redirect('course_detail', slug=course_slug)
        enrollment = Enrollment.objects.filter(user=request.user, course=course, is_active=True).first()
        if not enrollment:
            messages.error(request, "Avval kursga yoziling!")
            return redirect('course_detail', slug=course_slug)

    modules = course.modules.prefetch_related('lessons').all()
    progress = None
    if request.user.is_authenticated:
        progress, _ = LessonProgress.objects.get_or_create(user=request.user, lesson=lesson)

    if request.method == 'POST' and request.user.is_authenticated:
        if progress:
            progress.completed = True
            progress.completed_at = timezone.now()
            progress.save()
        return redirect('lesson_detail', course_slug=course_slug, lesson_id=lesson_id)

    all_lessons = []
    for m in modules:
        for l in m.lessons.all():
            all_lessons.append(l)

    current_idx = next((i for i, l in enumerate(all_lessons) if l.id == lesson.id), 0)
    prev_lesson = all_lessons[current_idx - 1] if current_idx > 0 else None
    next_lesson = all_lessons[current_idx + 1] if current_idx < len(all_lessons) - 1 else None

    return render(request, 'courses/lesson_detail.html', {
        'course': course,
        'lesson': lesson,
        'modules': modules,
        'prev_lesson': prev_lesson,
        'next_lesson': next_lesson,
        'progress': progress,
    })


# ---- Admin Views ----

@login_required
def manage_courses(request):
    if not request.user.is_admin():
        return redirect('home')
    courses = Course.objects.all().order_by('-created_at')
    return render(request, 'dashboard/courses.html', {'courses': courses})


@login_required
def course_create(request):
    if not request.user.is_admin():
        return redirect('home')
    form = CourseForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        course = form.save(commit=False)
        course.instructor = request.user
        course.save()
        messages.success(request, "Kurs yaratildi!")
        return redirect('course_modules', slug=course.slug)
    return render(request, 'dashboard/course_form.html', {'form': form, 'title': 'Yangi Kurs'})


@login_required
def course_edit(request, slug):
    if not request.user.is_admin():
        return redirect('home')
    course = get_object_or_404(Course, slug=slug)
    form = CourseForm(request.POST or None, request.FILES or None, instance=course)
    if form.is_valid():
        form.save()
        messages.success(request, "Kurs yangilandi!")
        return redirect('course_modules', slug=course.slug)
    return render(request, 'dashboard/course_form.html', {'form': form, 'title': 'Kursni Tahrirlash', 'course': course})


@login_required
def course_delete(request, slug):
    if not request.user.is_admin():
        return redirect('home')
    course = get_object_or_404(Course, slug=slug)
    if request.method == 'POST':
        course.delete()
        messages.success(request, "Kurs o'chirildi!")
        return redirect('manage_courses')
    return render(request, 'dashboard/confirm_delete.html', {'obj': course, 'type': 'course'})


@login_required
def course_modules(request, slug):
    if not request.user.is_admin():
        return redirect('home')
    course = get_object_or_404(Course, slug=slug)
    modules = course.modules.prefetch_related('lessons').all()
    module_form = ModuleForm()
    lesson_form = LessonForm()
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add_module':
            mf = ModuleForm(request.POST)
            if mf.is_valid():
                module = mf.save(commit=False)
                module.course = course
                module.order = modules.count() + 1
                module.save()
                messages.success(request, "Modul qo'shildi!")
        elif action == 'add_lesson':
            lf = LessonForm(request.POST, request.FILES)
            if lf.is_valid():
                lesson = lf.save()
                messages.success(request, "Dars qo'shildi!")
        elif action == 'delete_module':
            mid = request.POST.get('module_id')
            Module.objects.filter(id=mid, course=course).delete()
            messages.success(request, "Modul o'chirildi!")
        elif action == 'delete_lesson':
            lid = request.POST.get('lesson_id')
            Lesson.objects.filter(id=lid, module__course=course).delete()
            messages.success(request, "Dars o'chirildi!")
        return redirect('course_modules', slug=slug)
    return render(request, 'dashboard/course_modules.html', {
        'course': course,
        'modules': modules,
        'module_form': module_form,
        'lesson_form': lesson_form,
    })


@login_required
def manage_enrollments(request):
    if not request.user.is_admin():
        return redirect('home')
    enrollments = Enrollment.objects.select_related('user', 'course').order_by('-enrolled_at')
    course_filter = request.GET.get('course')
    if course_filter:
        enrollments = enrollments.filter(course__slug=course_filter)
    return render(request, 'dashboard/enrollments.html', {
        'enrollments': enrollments,
        'courses': Course.objects.all(),
    })


@login_required
def update_payment(request, enrollment_id):
    if not request.user.is_admin():
        return redirect('home')
    if request.method == 'POST':
        enrollment = get_object_or_404(Enrollment, id=enrollment_id)
        new_status = request.POST.get('payment_status')
        if new_status in ['pending', 'paid', 'free', 'cancelled']:
            enrollment.payment_status = new_status
            if new_status == 'paid':
                enrollment.payment_date = timezone.now()
            enrollment.save()
            messages.success(request, "To'lov holati yangilandi!")
    return redirect('manage_enrollments')


@login_required
def manage_students(request, slug):
    if not request.user.is_admin():
        return redirect('home')
    course = get_object_or_404(Course, slug=slug)
    enrollments = Enrollment.objects.filter(course=course).select_related('user')
    if request.method == 'POST':
        action = request.POST.get('action')
        uid = request.POST.get('user_id')
        if action == 'add':
            from apps.users.models import CustomUser
            username = request.POST.get('username')
            try:
                user = CustomUser.objects.get(username=username)
                Enrollment.objects.get_or_create(user=user, course=course, defaults={
                    'payment_status': 'free', 'is_active': True
                })
                if user.role == 'user':
                    user.role = 'student'
                    user.save()
                messages.success(request, f"{user.username} kursga qo'shildi!")
            except CustomUser.DoesNotExist:
                messages.error(request, "Foydalanuvchi topilmadi!")
        elif action == 'remove':
            Enrollment.objects.filter(user_id=uid, course=course).delete()
            messages.success(request, "O'quvchi kursdan chiqarildi!")
        return redirect('manage_students', slug=slug)
    return render(request, 'dashboard/students.html', {
        'course': course,
        'enrollments': enrollments,
    })
