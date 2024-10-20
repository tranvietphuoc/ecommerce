#!/bin/sh 

echo 'waiting for postgres...'

while ! nc -z $DB_HOSTNAME $DB_PORT; do 
    sleep 0.1
done 

echo 'PostgreSQL started'

echo 'running migration...'
python manage.py migrate

echo 'collecting static files...'
python manage.py collectstatic --no-input

exec "$@"
