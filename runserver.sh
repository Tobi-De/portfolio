python manage.py migrate
python manage.py makesuperuser
gunicorn config.wsgi:application --bind=0.0.0.0:80
