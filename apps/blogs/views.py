from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Blog, Tag
from .forms import BlogForm
from apps.contacts.models import SiteSettings


def home(request):
    blogs = Blog.objects.filter(is_published=True).order_by('-created_at')[:6]
    return render(request, 'home.html', {'blogs': blogs})


def about(request):
    return render(request, 'about.html')


def blog_list(request):
    blogs = Blog.objects.filter(is_published=True).order_by('-created_at')
    tag_slug = request.GET.get('tag')
    selected_tag = None
    if tag_slug:
        selected_tag = get_object_or_404(Tag, slug=tag_slug)
        blogs = blogs.filter(tags=selected_tag)
    paginator = Paginator(blogs, 6)
    page = request.GET.get('page', 1)
    blogs_page = paginator.get_page(page)
    tags = Tag.objects.all()
    return render(request, 'blogs/blog_list.html', {
        'blogs': blogs_page,
        'tags': tags,
        'selected_tag': selected_tag,
    })


def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug, is_published=True)
    blog.views_count += 1
    blog.save(update_fields=['views_count'])
    related = Blog.objects.filter(is_published=True).exclude(pk=blog.pk)[:3]
    return render(request, 'blogs/blog_detail.html', {'blog': blog, 'related': related})


@login_required
def blog_create(request):
    if not request.user.is_admin():
        messages.error(request, "Ruxsat yo'q!")
        return redirect('blog_list')
    form = BlogForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        blog = form.save(commit=False)
        blog.author = request.user
        blog.save()
        form.save_m2m()
        messages.success(request, "Blog yaratildi!")
        return redirect('blog_detail', slug=blog.slug)
    return render(request, 'dashboard/blog_form.html', {'form': form, 'title': 'Yangi Blog'})


@login_required
def blog_edit(request, slug):
    if not request.user.is_admin():
        messages.error(request, "Ruxsat yo'q!")
        return redirect('blog_list')
    blog = get_object_or_404(Blog, slug=slug)
    form = BlogForm(request.POST or None, request.FILES or None, instance=blog)
    if form.is_valid():
        form.save()
        messages.success(request, "Blog yangilandi!")
        return redirect('blog_detail', slug=blog.slug)
    return render(request, 'dashboard/blog_form.html', {'form': form, 'title': 'Blogni Tahrirlash', 'blog': blog})


@login_required
def blog_delete(request, slug):
    if not request.user.is_admin():
        return redirect('blog_list')
    blog = get_object_or_404(Blog, slug=slug)
    if request.method == 'POST':
        blog.delete()
        messages.success(request, "Blog o'chirildi!")
        return redirect('blog_list')
    return render(request, 'dashboard/confirm_delete.html', {'obj': blog, 'type': 'blog'})
