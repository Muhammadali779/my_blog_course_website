#!/bin/bash

echo "======================================"
echo "  Blog Platform - Setup"
echo "======================================"

# Create virtual environment if not exists
if [ ! -d ".venv" ]; then
    echo "Virtual environment yaratilmoqda..."
    python3 -m venv .venv
fi

# Activate venv
source .venv/bin/activate

echo "Paketlar o'rnatilmoqda..."
pip install -r requirements.txt --quiet

echo "Migratsiyalar yaratilmoqda..."
python manage.py makemigrations users
python manage.py makemigrations blogs
python manage.py makemigrations courses
python manage.py makemigrations contacts
python manage.py migrate

echo "Boshlang'ich ma'lumotlar yuklanmoqda..."
python manage.py setup_initial

echo ""
echo "======================================"
echo "  ✅ Setup tugadi!"
echo "  Server ishga tushirish:"
echo "  source .venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo "  Dashboard: http://localhost:8000/users/dashboard/"
echo "  Login: owner / Owner@123456"
echo "======================================"
