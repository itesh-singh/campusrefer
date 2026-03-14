#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
echo "from accounts.models import User; User.objects.create_superuser('itesh', 'itesh@admin.com', 'Admin@1234') if not User.objects.filter(username='itesh').exists() else print('exists')" | python manage.py shell