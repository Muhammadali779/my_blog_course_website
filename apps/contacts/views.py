from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ContactMessage, SiteSettings
from .forms import ContactForm


def contact_view(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Xabaringiz yuborildi! Tez orada javob beramiz.")
        return redirect('contact')
    return render(request, 'contact.html', {'form': form})


@login_required
def contact_list(request):
    if not request.user.is_admin():
        return redirect('home')
    messages_qs = ContactMessage.objects.all()
    unread = messages_qs.filter(is_read=False).count()
    return render(request, 'dashboard/contacts.html', {'messages': messages_qs, 'unread': unread})


@login_required
def mark_read(request, pk):
    if not request.user.is_admin():
        return redirect('home')
    msg = get_object_or_404(ContactMessage, pk=pk)
    msg.is_read = True
    msg.save()
    return redirect('contact_list')


@login_required
def site_settings_view(request):
    if not request.user.is_owner():
        messages.error(request, "Faqat Owner sozlamalarni o'zgartira oladi!")
        return redirect('admin_dashboard')
    settings_obj, _ = SiteSettings.objects.get_or_create(pk=1)
    from .forms import SiteSettingsForm
    form = SiteSettingsForm(request.POST or None, request.FILES or None, instance=settings_obj)
    if form.is_valid():
        form.save()
        messages.success(request, "Sozlamalar saqlandi!")
        return redirect('site_settings')
    return render(request, 'dashboard/site_settings.html', {'form': form})
