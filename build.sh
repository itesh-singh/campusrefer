#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input --skip-checks 2>/dev/null || true
python manage.py migrate