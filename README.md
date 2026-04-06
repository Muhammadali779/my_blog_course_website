# Blog Platform - Django

Personal portfolio + blog + courses platform.

## Tezkor ishga tushirish

```bash
# 1. Virtual environment yarating
python3 -m venv .venv
source .venv/bin/activate   # Linux/Mac
# .venv\Scripts\activate    # Windows

# 2. Paketlarni o'rnating
pip install -r requirements.txt

# 3. Migratsiyalar
python manage.py makemigrations users blogs courses contacts
python manage.py migrate

# 4. Boshlang'ich ma'lumotlar + Owner akkaunt
python manage.py setup_initial

# 5. Serverni ishga tushiring
python manage.py runserver
```

Ochiq: http://localhost:8000  
Dashboard: http://localhost:8000/users/dashboard/  
Admin panel: http://localhost:8000/admin/  
Login: `owner` / `Owner@123456`

---

## PostgreSQL ishlatish (ixtiyoriy)

`.env` faylni oching va o'zgartiring:

```
DB_ENGINE=postgresql
DB_NAME=my_blog_website
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

Keyin PostgreSQL'da database yarating:
```sql
CREATE DATABASE my_blog_website;
```

---

## Tuzatilgan xatoliklar

1. **`migrations` papkalari yo'q edi** — har bir app uchun `migrations/` va `migrations/__init__.py` yaratildi
2. **`settings.py` PostgreSQL hardcode** — `.env` orqali SQLite (default) yoki PostgreSQL tanlash imkoni qo'shildi
3. **`courses/models.py` `get_lessons_count()` xatosi** — `Sum('lessons__id')` noto'g'ri, tuzatildi
4. **`contacts/forms.py` widgets dict mutation** — to'g'ri `widgets` dict bilan qayta yozildi
5. **`.venv` papkasi** — zip'da `.venv` bo'lmasligi kerak, tozalandi
6. **`setup.sh`** — to'liq avtomatik setup skripti yozildi

## Struktura

```
blog_platform/
├── apps/
│   ├── users/       # CustomUser, login/register/profile
│   ├── blogs/       # Blog, Tag
│   ├── courses/     # Course, Module, Lesson, Enrollment
│   └── contacts/    # ContactMessage, SiteSettings
├── config/          # settings, urls, wsgi
├── templates/       # HTML shablonlar
├── static/          # CSS, JS
├── media/           # Yuklangan fayllar
├── .env             # Muhit o'zgaruvchilari
├── requirements.txt
└── manage.py
```
