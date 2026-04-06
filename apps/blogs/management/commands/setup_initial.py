from django.core.management.base import BaseCommand
from apps.users.models import CustomUser
from apps.blogs.models import Tag
from apps.courses.models import Category
from apps.contacts.models import SiteSettings


class Command(BaseCommand):
    help = "Boshlang'ich ma'lumotlarni yaratadi va owner akkaunt sozlaydi"

    def add_arguments(self, parser):
        parser.add_argument('--username', default='owner')
        parser.add_argument('--password', default='Owner@123456')
        parser.add_argument('--email', default='owner@example.com')

    def handle(self, *args, **options):
        # SiteSettings
        s, created = SiteSettings.objects.get_or_create(pk=1)
        if created or not s.skills:
            s.owner_name = 'Muhammadali'
            s.owner_title = 'Software Engineer | Django & Python Developer'
            s.owner_bio = (
                "Toshkent Axborot Texnologiyalari Universiteti Samarqand filialining "
                "Dasturiy Injiniring yo'nalishi talabasi. Python, Django, FastAPI, "
                "PostgreSQL va Aiogram texnologiyalari bilan ishlashni yaxshi ko'raman."
            )
            s.university = "Toshkent Axborot Texnologiyalari Universiteti Samarqand filiali"
            s.major = "Dasturiy Injiniring (Software Engineering)"
            s.skills = "Python, Django, FastAPI, PostgreSQL, Aiogram, C++, Git, Docker"
            s.save()
            self.stdout.write(self.style.SUCCESS("✅ SiteSettings sozlandi"))

        # Tags
        tags = ['Python', 'Django', 'PostgreSQL', 'FastAPI', 'JavaScript', 'Linux', 'Git', 'Docker', 'API', 'Backend']
        for name in tags:
            Tag.objects.get_or_create(name=name, defaults={'slug': name.lower().replace('+', 'plus').replace(' ', '-')})
        self.stdout.write(self.style.SUCCESS(f"✅ {len(tags)} ta teg yaratildi"))

        # Categories
        cats = [
            ('Backend', 'backend'), ('Frontend', 'frontend'),
            ('Database', 'database'), ('DevOps', 'devops'),
            ('Algorithms', 'algorithms'), ('Mobile', 'mobile'),
        ]
        for name, slug in cats:
            Category.objects.get_or_create(name=name, defaults={'slug': slug})
        self.stdout.write(self.style.SUCCESS(f"✅ {len(cats)} ta kategoriya yaratildi"))

        # Owner user
        username = options['username']
        password = options['password']
        email = options['email']

        if CustomUser.objects.filter(username=username).exists():
            user = CustomUser.objects.get(username=username)
            if user.role != 'owner':
                user.role = 'owner'
                user.is_staff = True
                user.is_superuser = True
                user.save()
                self.stdout.write(self.style.SUCCESS(f"✅ '{username}' roli 'owner' ga o'zgartirildi"))
            else:
                self.stdout.write(self.style.WARNING(f"⚠️  '{username}' allaqachon mavjud"))
        else:
            user = CustomUser.objects.create_superuser(
                username=username, email=email, password=password, role='owner'
            )
            self.stdout.write(self.style.SUCCESS(
                f"✅ Owner yaratildi:\n   Username: {username}\n   Password: {password}\n"
                f"   ⚠️  Parolni o'zgartiring!"
            ))

        self.stdout.write(self.style.SUCCESS("\n🚀 Barcha boshlang'ich ma'lumotlar tayyor!"))
        self.stdout.write("   Server: python manage.py runserver")
        self.stdout.write(f"   Dashboard: http://localhost:8000/users/dashboard/")
        self.stdout.write(f"   Login: {username} / {password}")
