#!/bin/sh

python manage.py collectstatic --noinput
python manage.py migrate
gunicorn config.wsgi --bind=127.0.0.11:80
