from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import CustomUser
from .forms import RegisterForm, LoginForm, ProfileUpdateForm, AdminCreateUserForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Muvaffaqiyatli ro'yxatdan o'tdingiz!")
        return redirect('home')
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = LoginForm(request.POST or None)
    next_url = request.GET.get('next', '/')
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Xush kelibsiz, {user.username}!")
            return redirect(next_url)
        else:
            messages.error(request, "Login yoki parol noto'g'ri!")
    return render(request, 'users/login.html', {'form': form, 'next': next_url})


def course_login_view(request):
    """Special login for course access"""
    form = LoginForm(request.POST or None)
    next_url = request.GET.get('next', '/courses/')
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.is_student():
                messages.success(request, "Kursga kirish huquqi tasdiqlandi!")
                return redirect(next_url)
            else:
                messages.error(request, "Siz hali kursga yozilmagansiz!")
        else:
            messages.error(request, "Login yoki parol noto'g'ri!")
    return render(request, 'users/course_login.html', {'form': form, 'next': next_url})


def logout_view(request):
    logout(request)
    messages.info(request, "Tizimdan chiqdingiz.")
    return redirect('home')


@login_required
def profile_view(request):
    form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, "Profil yangilandi!")
        return redirect('profile')
    return render(request, 'users/profile.html', {'form': form})


@login_required
def admin_dashboard(request):
    if not request.user.is_admin():
        messages.error(request, "Ruxsat yo'q!")
        return redirect('home')
    from apps.blogs.models import Blog
    from apps.courses.models import Course, Enrollment
    from apps.contacts.models import ContactMessage
    context = {
        'total_users': CustomUser.objects.count(),
        'total_blogs': Blog.objects.count(),
        'total_courses': Course.objects.count(),
        'total_messages': ContactMessage.objects.filter(is_read=False).count(),
        'recent_users': CustomUser.objects.order_by('-date_joined')[:10],
        'enrollments': Enrollment.objects.select_related('user', 'course').order_by('-enrolled_at')[:20],
    }
    return render(request, 'dashboard/dashboard.html', context)


@login_required
def manage_users(request):
    if not request.user.is_admin():
        return redirect('home')
    users = CustomUser.objects.all().order_by('-date_joined')
    return render(request, 'dashboard/users.html', {'users': users})


@login_required
def create_user(request):
    if not request.user.is_owner():
        messages.error(request, "Faqat Owner yangi admin qo'sha oladi!")
        return redirect('admin_dashboard')
    form = AdminCreateUserForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Yangi foydalanuvchi yaratildi!")
        return redirect('manage_users')
    return render(request, 'dashboard/create_user.html', {'form': form})


@login_required
@require_POST
def change_user_role(request, user_id):
    if not request.user.is_owner():
        messages.error(request, "Ruxsat yo'q!")
        return redirect('manage_users')
    target = get_object_or_404(CustomUser, id=user_id)
    new_role = request.POST.get('role')
    if new_role in ['admin', 'student', 'user']:
        target.role = new_role
        target.save()
        messages.success(request, f"{target.username} roli {new_role} ga o'zgartirildi!")
    return redirect('manage_users')


@login_required
@require_POST
def toggle_user_active(request, user_id):
    if not request.user.is_admin():
        return redirect('home')
    target = get_object_or_404(CustomUser, id=user_id)
    if target != request.user:
        target.is_active = not target.is_active
        target.save()
        status = "faollashtirildi" if target.is_active else "bloklandi"
        messages.success(request, f"{target.username} {status}!")
    return redirect('manage_users')
