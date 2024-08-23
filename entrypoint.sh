#!/bin/bash
# entrypoint.sh

# Wait for the database to be ready
echo "Waiting for the database to be ready..."
while ! nc -z $DB_HOST $DB_PORT; do
  echo "Database is unavailable - sleeping"
  sleep 1
done
echo "Database is up - continuing"

# Run Django management commands
echo "Making migrations..."
python geo_project/manage.py makemigrations

echo "Applying database migrations..."
python geo_project/manage.py migrate

# Start the Django development server
echo "Starting the Django development server..."
exec python geo_project/manage.py runserver 0.0.0.0:8000
