#!/bin/sh 

echo 'waiting for postgres...'

while ! nc -z $DB_HOST $DB_PORT; do

    sleep 0.1

done

echo 'PostgreSQL started'

echo 'running migration...'
# python manage.py makemigrations
python manage.py migrate --fake-initial

echo 'collecting static files...'
python manage.py collectstatic --no-input

exec "$@"
