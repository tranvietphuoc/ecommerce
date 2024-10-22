#!/bin/sh 

echo 'waiting for postgres...'

while ! nc -z $DB_HOST $DB_PORT; do

    sleep 1

done


# Wait for Redis to be ready
until nc -z redis 6379; do
  echo "Waiting for Redis..."
  sleep 1
done

echo 'PostgreSQL started'

echo 'running migration...'
python manage.py makemigrations
python manage.py migrate --fake-initial

echo 'collecting static files...'
python manage.py collectstatic --no-input

echo 'running server...'
python manage.py runserver 0.0.0.0:8000

exec "$@"
