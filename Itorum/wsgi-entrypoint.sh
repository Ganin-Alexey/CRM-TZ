#! /bin/bash

python ./manage.py makemigrations --no-input
python ./manage.py migrate --no-input
python ./manage.py collectstatic --noinput

python ./manage.py runserver 0.0.0.0:8000

#exec gunicorn  --chdir django_app mainapp.wsgi:application --bind 0.0.0.0:8000 --workers 4 --threads 4 --reload
